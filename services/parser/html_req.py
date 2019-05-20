# -*- coding: utf-8 -*-

import requests
from lxml import etree
from lxml import html
from services.store.proxy import ProxyProvider


class HtmlRequests():
    def __init__(self):
        self.__pv = ProxyProvider()

    def get_sourcehtml(self, source_url):
        for i in range(5):
            proxy = self.__pv.get_proxy()
            if proxy == None:
                with requests.get(source_url) as r:
                    if r.status_code == 200:
                        return html.fromstring(r.text)
            else:
                with requests.get(source_url, timeout=30, proxies=proxy["ip"], headers=proxy["headers"]) as r:
                    if r.status_code == 200:
                        return html.fromstring(r.text)
        else:
            print("Fail to get %s" % (source_url))

    def get_sourcehtml_noproxy(self, source_url):
        for i in range(5):
            with requests.get(source_url) as r:
                if r.status_code == 200:
                    return html.fromstring(r.text)
        else:
            print("Fail to get %s" % (source_url))
