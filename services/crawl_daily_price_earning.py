from services.parser.html_req import HtmlRequests
from store.mongo import MongodbAPI
from datetime import datetime
import time
import json
import threading
import requests
import logging

DAILYSTOCKINFO = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date={date}&type=ALL"


class Daily_stock_info(object):
    def __init__(self, date):
        self.__mongo = MongodbAPI()
        self.__htmlreq = HtmlRequests()
        self.__date = date
        pass

    def start(self):
        date = self.__date.strftime("%Y%m%d")
        source_url = DAILYSTOCKINFO.format(date=date)
        data = self.__crawl(source_url, self.__date.strftime("%Y/%m/%d"))
        if data != None:
            err = self.__mongo.Insert_Many_Data_To('stock_daily_info', data)
            if err:
                logging.info(
                    "Insert stock daily info to mongo , date: %s", date)
            else:
                logging.warn(
                    "Fail to Insert stock daily info to mongo , url: %s", source_url)
        return

    def __crawl(self, url, date):
        j = self.__htmlreq.get_json(requests, url)
        if j == {} or j['stat'] != 'OK':
            return None
        data = self.__parser(date, j)
        return data

    def __parser(self, date, j: json) -> list:
        rows = [x for x in j['data5'] if len(x[0]) == 4 and x[-1] != '0.00']
        data = []
        for i in rows:
            data.append({
                '_id': i[0]+"@"+date,
                'stock': i[0],
                'date': datetime.strptime(date, "%Y/%m/%d"),
                'ts': int(datetime.timestamp(datetime.strptime(date, "%Y/%m/%d"))),
                'price_earning': float(i[-1].replace(',', ''))
            })
        return data
