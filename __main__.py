# -*- coding: utf-8 -*-
from twstock import Stock,realtime
from services.crawl_proxy import Crawl_Proxy

def main():
    cp = Crawl_Proxy("http://www.cybersyndrome.net/search.cgi?q=&a=ABCD&f=s&s=new&n=500")
    cp.Start()
    # stock = Stock('3535')                             # 擷取台積電股價
    # print(stock.fetch_from(2019, 4))
    # print(realtime.get('3535'))

if __name__ == '__main__':
    main()