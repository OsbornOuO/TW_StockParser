# -*- coding: utf-8 -*-

from lxml import etree
from lxml import html
from store.mongo import MongodbAPI
from .parser.html_req import HtmlRequests
import requests
import re
import math
from datetime import datetime, timedelta
import logging

CYBERSYNDROME = "http://www.cybersyndrome.net/search.cgi?q=&a=ABC&f=d&s=new&n=500"


class Crawl_Proxy(object):
    def __init__(self):
        self.source_url = CYBERSYNDROME
        self.mongo = MongodbAPI()

    def start(self):
        data = self.mongo.Get_Data_From("proxy", {'id': 0})
        if data is not None and datetime.now()-timedelta(hours=3) < data["update_date"]:
            logging.info("Use old proxies")
            return
        logging.info("start crawl proxy")
        self.mongo.DropAll("proxy")
        proxy_ip = self.paresrHTML()
        self.mongo.Insert_Data_To("proxy", {
            "id": 0,
            "iptable": proxy_ip,
            "update_date": datetime.now()
        })
        logging.info("add %04d ip" % (len(proxy_ip)))

    def paresrHTML(self):
        p = HtmlRequests()
        tree = p.get_html_noproxy(self.source_url)
        _as = []
        _ps = []
        if tree == None:
            return
        for i in tree.xpath('//div[@id="content"]/script/text()'):
            result = re.findall('\[[0-9 ,]*\]', i)
            _as = result[0].replace("[", '').replace("]", '')
            _ps = result[1].replace("[", '').replace("]", '')
            _as_list = [x for x in _as.split(',')]
            _ps_list = [x for x in _ps.split(',')]
            arithmetic = re.findall('\(.*?\)%\d*', i)
            n = self.decode(_ps_list, arithmetic[0])
            _as = _as_list[n:] + _as_list[0:n]
            break
        headerlist = []
        for i in tree.xpath('//tr'):
            headers = {}
            for j in i.xpath('td[6]/text()'):
                tmp = j.split(":")
                headers[tmp[0]] = tmp[1]
            headerlist.append(headers)
        return self.getproxy(_as, _ps_list, headerlist)

    def decode(self, ps, string):
        divisor = string.split(')')[1].replace('%', '')
        dividend = string.split(')')[0].replace('(', '')
        num = 0
        for i in dividend.split('+'):
            if "*" in i:
                mult = 1
                for k in i.split('*'):
                    if "ps" in k:
                        count = int(re.search('\d+', k).group(0))
                        mult *= int(ps[count])
                    else:
                        mult *= int(k)
                num += mult
            else:
                if "ps" in i:
                    count = int(re.search('\d+', i).group(0))
                    num += int(ps[count])
                else:
                    num += int(i)
        return num % int(divisor)

    def getproxy(self, _as, _ps, headerlist):
        proxy_ip = []
        j = 0
        ip = ""
        for i in range(len(_as)):
            if i % 4 == 3:
                ip += _as[i]
                proxy_ip.append({
                    'ip': {
                        'http': ip+':'+_ps[j]
                    },
                    'headers': headerlist[j]
                })
                j += 1
                ip = ""
                continue
            ip += _as[i]+'.'
        return proxy_ip
