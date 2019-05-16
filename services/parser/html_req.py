# -*- coding: utf-8 -*-

import requests
from lxml import etree
from lxml import html

class HtmlRequests():
    def __init__(self,source_url):
        self.source_url = source_url
    def get_sourcehtml(self):
        with requests.get(self.source_url) as r:
            if r.status_code == 200:
                return html.fromstring(r.text);
            else:
                return None
