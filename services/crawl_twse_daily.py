from services.parser.html_req import HtmlRequests
from store.mongo import MongodbAPI
from datetime import datetime
import time
import json
import threading
import requests
import logging

SESSIONURL = 'http://mis.twse.com.tw/stock/index.jsp'
TWSEREALTIMEURL = "http://www.twse.com.tw/exchangeReport/STOCK_DAY?date={time}&stockNo={stock_num}"


class TWSE_daily():
    def __init__(self, stock_num: str, start_year: int, start_month: int):
        self.mongo = MongodbAPI()
        self.stock_num = stock_num
        self.htmlreq = HtmlRequests()
        self.req = self.htmlreq.get_session(SESSIONURL)
        self.req.keep_alive = False
        self.start_year = start_year
        self.start_month = start_month
        self.now_date = datetime.now()
        self.retry = 0

    def start(self):
        now_year = self.start_year
        now_month = self.start_month
        self.crawl(now_year, now_month)

    def crawl(self, year, month):
        logging.debug("%s/%s" % (year, month))
        source_url = TWSEREALTIMEURL.format(
            stock_num=self.stock_num, time="%d%02d01" % (year, month))
        json_data = self.htmlreq.get_json(self.req, source_url)
        if json_data == {} and self.retry < 5:
            self.retry += 1
            self.crawl(year, month)
        else:
            logging.error("Can't get old daily stock %s@%s-%s ,url : %s " %
                          (self.stock_num, year, month, source_url))
        self.retry = 0
        data = self.parser(json_data.get('data', None))

        if data != None and len(data) > 0:
            for i in range(5):
                err = self.mongo.Insert_Many_Data_To("Daily_data", data)
                if err == True:
                    logging.info("Insert Daily data %s@%s-%s" %
                                 (self.stock_num, year, month))
                    break
            else:
                logging.error("Fail, Insert Daily data to Mongo,id: %s@%s-%s" %
                              (self.stock_num, year, month))
        date = self._get_next_date(year, month)
        if date['year'] >= self.now_date.year and date['month'] > self.now_date.month:
            logging.info("Done crawl Daily data , %s@%s/%s" %
                         (self.stock_num, date['year'], date['month']))
            return
        # Start to crawl new year, month
        self.crawl(date["year"], date["month"])

    def _convert_date(self, date):
        """Convert '106/05/01' to '2017/05/01'"""
        return '/'.join([str(int(date.split('/')[0]) + 1911)] + date.split('/')[1:])

    def parser(self, j: json) -> list:
        data = []
        if j == None:
            return data
        for item in j:
            date = datetime.strptime(
                self._convert_date(item[0]), '%Y/%m/%d')
            _id = self.stock_num + "@"+date.strftime("%Y/%m/%d")

            e = self.mongo.CheckExists(
                "Daily_data", _id)
            if e:
                logging.debug("Insert Daily data ,id :%s exists" %
                              (_id))
                continue
            try:
                data.append({
                    '_id': _id,
                    'stock': self.stock_num,
                    'date': date,
                    'ts': int(time.mktime(date.timetuple())),
                    'capacity': int(item[1].replace(',', '')),
                    'turnover': int(item[2].replace(',', '')),
                    'open': self._get_float(item[3]),
                    'high': self._get_float(item[4]),
                    'low': self._get_float(item[5]),
                    'close':  self._get_float(item[6]),
                    'change':  self._get_float(item[7]),
                    'transaction': int(item[8].replace(',', ''))
                })
            except Exception as e:
                logging.error("daily data fail :{} {}" % (item, e))
                continue
        return data

    def _get_next_date(self, year, month) -> dict:
        if month < 12:
            month += 1
        else:
            year += 1
            month = 1
        return {
            'year': year,
            'month': month
        }

    def _get_float(self, number: str):
        if number.replace(',', '') == 'X0.00':
            return 0.0
        elif number == '--':
            return None
        else:
            return float(number.replace(',', ''))
        return
