# -*- coding: utf-8 -*-

from lxml import etree
from lxml import html
from .store.mongo import MongodbAPI
from .parser.html_req import HtmlRequests
import requests
import re
import math
from datetime import datetime, timedelta


class Crawl_Proxy(object):
    def __init__(self, url):
        self.source_url = url
        self.mongo = MongodbAPI()

    def Start(self):
        data = self.mongo.Get_Data_From("proxy", {'id': 0})
        if datetime.now()-timedelta(hours=6) < data["update_date"]:
            return
        self.mongo.DropAll("proxy")
        proxy_ip = self.paresrHTML()
        self.mongo.Insert_Data_To("proxy", {
            "id": 0,
            "ip": proxy_ip,
            "update_date": datetime.now()
        })
        print("add", len(proxy_ip), "ip")

    def paresrHTML(self):
        p = HtmlRequests(self.source_url)
        tree = p.get_sourcehtml()
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
            return self.getproxy(_as, _ps_list)

    def decode(self, ps, string):
        divisor = string.split(')')[1].replace('%', '')
        dividend = string.split(')')[0].replace('(', '')
        variable = re.findall('ps\[(\d*)\]', dividend)
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

    def getproxy(self, _as, _ps):
        proxy_ip = []
        j = 0
        ip = ""
        for i in range(len(_as)):
            if i % 4 == 3:
                ip += _as[i]
                proxy_ip.append(ip+':'+_ps[j])
                j += 1
                ip = ""
                continue
            ip += _as[i]+'.'
        return proxy_ip
