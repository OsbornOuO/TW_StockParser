# -*- coding: utf-8 -*-

from services.parser.html_req import HtmlRequests
from services.store.mongo import MongodbAPI

import re
from datetime import datetime
url = "https://ww2.money-link.com.tw/TWStock/StockTick.aspx?SymId=%d#SubMain"

retry = 5


class Money_link():
    def __init__(self):
        self.mongo = MongodbAPI()

    def Start(self, stock_num) -> list:
        source_url = url % (stock_num)
        return self.parser(stock_num, source_url)

    def parser(self, stock_num, url) -> list:
        daily = []
        htmlparser = HtmlRequests()
        tree = htmlparser.get_sourcehtml(url)
        if tree == None:
            return daily
        now = datetime.now()
        for i in tree.xpath('//div[@id="TickHeight"]/table/tr'):
            time = i.xpath('td[1]/text()')[0]
            buying = i.xpath('td[2]/text()')[0]
            selling = i.xpath('td[3]/text()')[0]
            if buying == '--' or selling == '--':
                continue
            transaction = i.xpath('td[4]/text()')[0]
            tmp_ups_and_downs = i.xpath('td[5]/text()')[0].split(" ")
            ups_and_downs = ""
            if len(tmp_ups_and_downs) < 2:
                ups_and_downs = "0.0"
            elif tmp_ups_and_downs[0] == "▼":
                ups_and_downs = "-"+tmp_ups_and_downs[1]
            elif tmp_ups_and_downs[0] == "▲":
                ups_and_downs = tmp_ups_and_downs[1]
            stock_volume = i.xpath('td[6]/text()')[0]
            time_tmp = time.split(':')
            date = datetime(now.year, now.month, now.day,
                            int(time_tmp[0]), int(time_tmp[1]), int(time_tmp[2]))
            if self.mongo.CheckExists("Transaction_details", str(stock_num)+"@"+date.isoformat()):
                continue
            daily.append({
                '_id': str(stock_num)+"@"+date.isoformat(),
                'date': date,
                'buying': float(buying),
                'selling': float(selling),
                'transaction': float(transaction),
                'ups_and_downs': float(ups_and_downs),
                'stock_volume': int(stock_volume)
            })
        return daily
