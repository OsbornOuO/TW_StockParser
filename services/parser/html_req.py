# -*- coding: utf-8 -*-

from lxml import etree
from lxml import html
from store.proxy import get_proxy, delete_proxy
from fake_useragent import UserAgent

import requests
import random
import time
import logging


class HtmlRequests():
    def __init__(self):
        self.ua = UserAgent(use_cache_server=False)

    def get_html(self, source_url):
        r = self.__http_requests(requests, source_url)
        return html.fromstring(r.text)

    def get_html_noproxy(self, source_url: str):
        for i in range(5):
            with requests.get(source_url) as r:
                if r.status_code == 200:
                    return html.fromstring(r.text)
        else:
            logging.error("Fail to get %s" % (source_url))

    def get_json(self, req, source_url: str) -> dict:
        data = self.__http_requests(req, source_url)
        if data == None:
            return {}
        else:
            try:
                j = data.json()
                return j
            except Exception:
                logging.error(
                    "Fail response -> json,url: %s , status_code: %d " % (data.url, data.status_code))
                return {}

    def get_session(self, source_url: str) -> object:
        req = requests.Session()
        for i in range(10):
            try:
                proxy = get_proxy()
                r = req.get(source_url, timeout=30,
                            proxies=proxy["ip"], headers=proxy["headers"])
                if r.status_code == 200:
                    return req
            except Exception as e:
                logging.warn("Can't get session, err:%s" % (e))
                delete_proxy(proxy)
                continue
        else:
            logging.error("Can't get session from %s " % (source_url))

    def __http_requests(self, req: requests, url: str):
        for i in range(10):
            proxy = {}
            try:
                proxy = get_proxy()
                headers = proxy.get('headers', None)
                headers.update({
                    'Connection': 'close',
                    'HTTP_CONNECTION': 'close',
                    'User-Agent': self.ua.random
                })
                sleep = 5 + random.uniform(5, 10)
                with req.get(url,
                             timeout=30,
                             proxies=proxy.get('ip', None),
                             headers=headers) as r:
                    if r.status_code == 200:
                        time.sleep(sleep)
                        return r
                time.sleep(sleep)
            except Exception:
                delete_proxy(proxy)
                continue
        else:
            logging.error("Fail to get %s" % (url))
            return None
