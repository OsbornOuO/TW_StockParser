# -*- coding: utf-8 -*-

from twstock import Stock, realtime
from twstock.proxy import RoundRobinProxiesProvider, configure_proxy_provider
from twstock.proxy import get_proxies
from datetime import datetime

class parserTWStock():
    def __init__(self, stock_number, proxylist):
        self.stock = Stock(stock_number)
        self.stock_number = stock_number
        rrpr = RoundRobinProxiesProvider(proxylist)
        configure_proxy_provider(rrpr)

    def get_realtime(self):
        tmp = self.get_realtime_original()
        return {
            "_id": self.stock_number + "@"+tmp["info"]["time"],
            "code": int(self.stock_number),
            "time": datetime.strptime(tmp["info"]["time"], '%Y-%m-%d %H:%M:%S'),
            "latest_trade_price": float(tmp["realtime"]["latest_trade_price"]),
            "trade_volume": float(tmp["realtime"]["trade_volume"]),
            "accumulate_trade_volume": float(tmp["realtime"]["accumulate_trade_volume"]),
            "best_bid_price": [float(x) for x in tmp["realtime"]["best_bid_price"]],
            "best_bid_volume": [float(x) for x in tmp["realtime"]["best_bid_volume"]],
            "best_ask_price": [float(x) for x in tmp["realtime"]["best_ask_price"]],
            "best_ask_volume": [float(x) for x in tmp["realtime"]["best_ask_volume"]],
            "open": float(tmp["realtime"]["open"]),
            "high": float(tmp["realtime"]["high"]),
            "low": float(tmp["realtime"]["low"])
        }

    def get_oldprice(self):
        tmp = self.get_oldprice_original()
        data = []
        for x in tmp:
            data.append({
                '_id': self.stock_number +"@"+x.date.strftime("%Y/%m/%d"),
                'date': x.date,
                'capacity': x.capacity,
                'turnover': x.turnover,
                'open': x.open,
                'high': x.high,
                'low': x.low,
                'close': x.close,
                'change': x.change,
                'transaction': x.transaction
            })
        return data

    def get_realtime_original(self):
        try:
            tmp = realtime.get(self.stock_number)
            return tmp
        except:
            self.get_realtime()

    def get_oldprice_original(self):
        try:
            tmp = self.stock.fetch_from(2019, 5)
            return tmp
        except:
            self.get_oldprice()
