from services.parser.html_req import HtmlRequests
from store.mongo import MongodbAPI
from datetime import datetime
import time
import json
import threading
import requests
import logging

TSELEGALPERSON = "http://www.tse.com.tw/fund/T86?response=json&date={date}&selectType=ALLBUT0999"


class Institutional_investors ():
    def __init__(self, year, month, day):
        self.mongo = MongodbAPI()
        self.htmlreq = HtmlRequests()
        self._year = year
        self._month = month
        self._day = day
        pass

    def start(self):
        date = "%s%s%s" % (self._year, self._month, self._day)
        source_url = TSELEGALPERSON.format(date=date)
        self.__crawl(source_url, "%s/%s/%s" %
                     (self._year, self._month, self._day))
        pass

    def __crawl(self, url, date):
        json_data = self.htmlreq.get_json(requests, source_url=url)
        if json_data.get('stat', None) != "OK":
            logging.debug("This day not Opening :%s" % (date))
            return
        data = self.__parser(json_data, date)
        self.mongo.Insert_Many_Data_To("stock_information", data)
        pass

    def __parser(self, j, date) -> list:
        data = []
        for i in j['data']:
            i = [x.replace(',', '') for x in i]
            data.append({
                '_id': str(i[0])+"@"+date,
                'date': datetime.strptime(date, "%Y/%m/%d"),
                'stock_num': str(i[0]),
                'foreign_investment_buy': float(i[2]),
                'foreign_investment_sell': float(i[3]),
                'foreign_investment_net_buy_sell': float(i[4]),
                'foreign_investment_dealer_buy': float(i[5]),
                'foreign_investment_dealer_sell': float(i[6]),
                'foreign_investment_dealer_net_buy_sell': float(i[7]),
                'investment_trust_buy': float(i[8]),
                'investment_trust_sell': float(i[9]),
                'investment_trust_net_buy_sell': float(i[10]),
                'dealer_net_buy_sell': float(i[11]),
                'dealer_buy(Self-purchase)': float(i[12]),
                'dealer_sell(Self-purchase)': float(i[13]),
                'dealer_net_buy_sell(Self-purchase)': float(i[14]),
                'dealer_buy(Hedging)': float(i[15]),
                'dealer_sell(Hedging)': float(i[16]),
                'dealer_net_buy_sell(Hedging)': float(i[17]),
                'institutional_investors_net_buy_sell': float(i[18]),
            })
        return data
