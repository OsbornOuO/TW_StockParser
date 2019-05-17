# -*- coding: utf-8 -*-

from services.parser.html_req import HtmlRequests
import re
from datetime import datetime
url = "https://ww2.money-link.com.tw/TWStock/StockTick.aspx?SymId=%d#SubMain"


class Money_link():
    def Start(self, stock_num):
        source_url = url % (stock_num)
        return self.parser(stock_num, source_url)

    def parser(self, stock_num, url):
        htmlparser = HtmlRequests()
        tree = htmlparser.get_sourcehtml(url)
        daily = []
        now = datetime.now()
        for i in tree.xpath('//div[@id="TickHeight"]/table/tr'):
            time = i.xpath('td[1]/text()')[0]
            buying = i.xpath('td[2]/text()')[0]
            selling = i.xpath('td[3]/text()')[0]
            if buying == '--' or selling == '--':
                continue
            transaction = i.xpath('td[4]/text()')[0]
            tmp_ups_and_downs = i.xpath('td[5]/text()')[0]
            re_offset = "[0-9.]{1,4}"
            ups_and_downs = re.search(re_offset, tmp_ups_and_downs).group(0)
            stock_volume = i.xpath('td[6]/text()')[0]
            time_tmp = time.split(':')
            date = datetime(now.year, now.month, now.month,
                            int(time_tmp[0]), int(time_tmp[1]), int(time_tmp[2]))
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
