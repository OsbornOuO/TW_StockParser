# -*- coding: utf-8 -*-

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
        for i in range(10):
            j = self.__htmlreq.get_json(requests, url)
            if j == {} or j['stat'] != 'OK':
                return None

            rows = []
            if 'data5' in j:
                rows = [x for x in j['data5'] if len(
                    x[0]) == 4 and x[-1] != '0.00']
            elif 'data4' in j:
                rows = [x for x in j['data4'] if len(
                    x[0]) == 4 and x[-1] != '0.00']
            else:
                logging.warn(
                    "The daily info not have data5 or data4 url: %s", url)
                return None
            data = self.__parser(date, rows)
            return data
        else:
            logging.error("Fail to parser daily stock info , url: %s", url)

    def __parser(self, date, rows: list) -> list:
        data = []
        for i in rows:
            data.append({
                '_id': i[0]+"@"+date,
                'stock': i[0],
                'date': datetime.strptime(date, "%Y/%m/%d"),
                'ts': int(datetime.timestamp(datetime.strptime(date, "%Y/%m/%d"))),
                'transaction': float(i[3].replace(',', '')),
                'open': self.__get_float(i[5]),
                'high': self.__get_float(i[6]),
                'low': self.__get_float(i[7]),
                'close':  self.__get_float(i[8]),
                'change':  self.__get_sign_float(i[9], i[10]),
                'price_earning': float(i[-1].replace(',', '')),
            })
        return data

    def __get_sign_float(self, sign, num) -> float:
        if "-" in sign:
            return float("-"+num)
        elif "+" in sign:
            return float(num)
        else:
            return 0.0

    def __get_float(self, num) -> float:
        if num.replace(',', '') == 'X0.00':
            return 0.0
        elif num == '--':
            return None
        else:
            return float(num.replace(',', ''))
