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
            proxies = self.__pv.get_proxies()
            print(proxies)
            with requests.get(source_url, timeout=30, proxies=proxies) as r:
                if r.status_code == 200:
                    return html.fromstring(r.text)
        else:
            print("Fail to get %s" % (source_url))
