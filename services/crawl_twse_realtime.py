from services.parser.html_req import HtmlRequests
from services.store.mongo import MongodbAPI
from datetime import datetime
import time
import json
import threading

SESSIONURL = 'http://mis.twse.com.tw/stock/index.jsp'
TWSEREALTIMEURL = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_num}.tw&json=1&delay=0&_={time}"


class TWSE_realtime():
    def __init__(self, stock_num):
        self.mongo = MongodbAPI()
        self.stock_num = stock_num
        self.htmlreq = HtmlRequests()
        self.req = self.htmlreq.get_session(SESSIONURL)

    def start(self):
        self.crawl()

    def crawl(self):
        now = int(time.time()) * 1000
        source_url = TWSEREALTIMEURL.format(
            stock_num=self.stock_num, time=now)
        json_data = self.htmlreq.get_json(self.req, source_url)
        data = self.parser(json_data)
        e = self.mongo.CheckExists('Realtime_data', data.get('_id', None))
        if e == False:
            self.mongo.Insert_Data_To("Realtime_data", data)

    def parser(self, j: json):
        # Process best result
        data = j['msgArray'][0]

        def _split_best(d):
            if d:
                return d.strip('_').split('_')
            return d

        time = datetime.fromtimestamp(
            int(data['tlong']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return {
            "_id": str(self.stock_num) + "@"+time,
            "code": self.stock_num,
            "time": datetime.strptime(time, '%Y-%m-%d %H:%M:%S'),
            "latest_trade_price": float(data.get('z', None)),
            "trade_volume": float(data.get('tv', None)),
            "accumulate_trade_volume": float(data.get('v', None)),
            "best_bid_price": [float(x) for x in _split_best(data.get('b', None))],
            "best_bid_volume": [float(x) for x in _split_best(data.get('g', None))],
            "best_ask_price": [float(x) for x in _split_best(data.get('a', None))],
            "best_ask_volume": [float(x) for x in _split_best(data.get('f', None))],
            "open": float(data.get('o', None)),
            "high": float(data.get('h', None)),
            "low": float(data.get('l', None))
        }
