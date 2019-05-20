# -*- coding: utf-8 -*-

import requests
from lxml import etree
from lxml import html
from services.store.proxy import get_proxy


class HtmlRequests():
    def get_html(self, source_url):
        r = self.http_requests(requests, source_url)
        return self.http_requests(r.text)

    def get_html_noproxy(self, source_url: str):
        for i in range(5):
            with requests.get(source_url) as r:
                if r.status_code == 200:
                    return html.fromstring(r.text)
        else:
            print("Fail to get %s" % (source_url))

    def get_json(self, req, source_url: str) -> dict:
        return self.http_requests(req, source_url).json()

    def get_session(self, source_url: str) -> object:
        req = requests.Session()
        for i in range(5):
            try:
                proxy = get_proxy()
                r = req.get(source_url, timeout=10,
                            proxies=proxy["ip"], headers=proxy["headers"])
                if r.status_code == 200:
                    return req
            except:
                continue
        else:
            print("Can't get session from %s " % (source_url))

    def http_requests(self, req: requests, url: str):
        for i in range(5):
            try:
                proxy = get_proxy()
                with req.get(url,
                             timeout=30,
                             proxies=proxy.get('ip', None),
                             headers=proxy.get('headers', None)) as r:
                    if r.status_code == 200:
                        return r
            except:
                continue
        else:
            print("Fail to get %s" % (url))
