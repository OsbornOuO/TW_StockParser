# -*- coding: utf-8 -*-

import requests
from lxml import etree
from lxml import html
import random
import time
from services.store.proxy import get_proxy, delete_proxy


class HtmlRequests():
    def get_html(self, source_url):
        r = self.http_requests(requests, source_url)
        return html.fromstring(r.text)

    def get_html_noproxy(self, source_url: str):
        for i in range(5):
            with requests.get(source_url) as r:
                if r.status_code == 200:
                    return html.fromstring(r.text)
        else:
            print("Fail to get %s" % (source_url))

    def get_json(self, req, source_url: str) -> dict:
        data = self.http_requests(req, source_url)
        if data == None:
            return {}
        else:
            return data.json()

    def get_session(self, source_url: str) -> object:
        req = requests.Session()
        for i in range(10):
            try:
                proxy = get_proxy()
                r = req.get(source_url, timeout=15,
                            proxies=proxy["ip"], headers=proxy["headers"])
                if r.status_code == 200:
                    return req
            except Exception as e:
                print(e)
                delete_proxy(proxy)
                continue
        else:
            print("Can't get session from %s " % (source_url))

    def http_requests(self, req: requests, url: str):
        for i in range(10):
            proxy = {}
            try:
                proxy = get_proxy()
                headers = proxy.get('headers', None)
                headers.update({
                    'Connection': 'close',
                    'HTTP_CONNECTION': 'close'
                })
                sleep = 0.5 + random.uniform(0.1, 0.5)
                with req.get(url,
                             timeout=30,
                             proxies=proxy.get('ip', None),
                             headers=headers) as r:
                    if r.status_code == 200:
                        time.sleep(sleep)
                        return r
                time.sleep(sleep)
            except requests.ReadTimeout as e:
                delete_proxy(proxy)
            except requests.TooManyRedirects as e:
                delete_proxy(proxy)
            except Exception as e:
                print(e)
                continue
        else:
            print("Fail to get %s" % (url))
            return None
