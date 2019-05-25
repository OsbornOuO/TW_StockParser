from services.parser.html_req import HtmlRequests
from store.mongo import MongodbAPI
from datetime import datetime
import time
import json
import threading
import requests
import logging

TSELEGALPERSON = "http://www.tse.com.tw/fund/T86?response=json&date={date}&selectType=ALLBUT0999"


class LegalPerson():
    def __init__(self, year, month, day):
        self.mongo = MongodbAPI()
        self.htmlreq = HtmlRequests()

        pass

    def start(self):
        date = "%s%s%s" % ('2018', '01', '02')
        source_url = TSELEGALPERSON.format(date=date)
        self.crawl(source_url)
        pass

    def crawl(self, url):
        json_data = self.htmlreq.get_json(requests, source_url=url)
        print(json_data)
        pass

    def parser(self):
        pass
