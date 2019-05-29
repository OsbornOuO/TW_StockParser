# -*- coding: utf-8 -*-

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
    def __init__(self, date: datetime):
        self.mongo = MongodbAPI()
        self.htmlreq = HtmlRequests()
        self.__date = date
        pass

    def start(self):
        date = self.__date.strftime("%Y%m%d")
        source_url = TSELEGALPERSON.format(date=date)
        self.__crawl(source_url, self.__date.strftime("%Y/%m/%d"))
        pass

    def __crawl(self, url, date):
        json_data = self.htmlreq.get_json(requests, source_url=url)
        if json_data.get('stat', None) != "OK":
            logging.debug("This day not Opening :%s" % (date))
            return
        data = self.__parser(json_data, date)
        err = self.mongo.Insert_Many_Data_To("stock_information", data)
        if err:
            logging.info(
                "Insert Institutional investors to mongo , date: %s", date)
        else:
            logging.warn(
                "Fail to Insert Institutional investors to mongo , url: %s", url)

    def __parser(self, j, date) -> list:
        data = []
        for i in j['data']:
            i = [x.replace(',', '') for x in i]
            if len(j['fields']) == 12:
                data.append({
                    '_id': str(i[0])+"@"+date,
                    'date': datetime.strptime(date, "%Y/%m/%d"),
                    'stock_num': str(i[0]),
                    'foreign_investment_dealer_buy': float(i[2]),
                    'foreign_investment_dealer_sell': float(i[3]),
                    'foreign_investment_dealer_net_buy_sell': float(i[4]),
                    'institutional_investors_net_buy_sell': float(i[5]),
                    'investment_trust_buy': float(i[6]),
                    'investment_trust_sell': float(i[7]),
                    'investment_trust_net_buy_sell': float(i[8]),
                    'dealer_buy(Self-purchase)': float(i[9]),
                    'dealer_sell(Self-purchase)': float(i[10]),
                    'dealer_net_buy_sell': float(i[11]),
                })
            elif len(j['fields']) < 18:
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
                    'dealer_buy': float(i[12]),
                    'dealer_sell': float(i[13]),
                    'institutional_investors_net_buy_sell': float(i[14]),
                })
            elif len(j['fields']) == 18:
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
#['證券代號', '證券名稱', '外資買進股數', '外資賣出股數', '外資買賣超股數', '投信買進股數', '投信賣出股數', '投信買賣超股數', '自營商買賣超股數', '自營商買進股數', '自營商賣出股數', '三大法人買賣超股數']
