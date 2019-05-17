# -*- coding: utf-8 -*-

import requests
from lxml import etree
from lxml import html

class HtmlRequests():
    def get_sourcehtml(self,source_url):
        with requests.get(source_url) as r:
            if r.status_code == 200:
                return html.fromstring(r.text);
            else:
                return None
