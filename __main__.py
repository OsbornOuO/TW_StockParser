# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_twse import parserTWStock
from services.store.mongo import MongodbAPI
from services.crawl_money_link import Money_link
from services.crawl_twse_realtime import TWSE_realtime
from services.crawl_twse_daily import TWSE_daily
from services.store.proxy import close_proxy

import sys
import getopt
import threading


def money_link(m, ml, stock: list):
    print("start to parser stock :", stock)
    data = ml.start(stock)
    if len(data) is not 0:
        print("Insert daily detail stock:%s, count : %d" % (stock, len(data)))
        m.Insert_Many_Data_To("Transaction_details", data)


def twse_realtime(stock_num):
    print("start to parser stock :", stock_num)
    tr = TWSE_realtime(stock_num)
    tr.start()


def twse_daily(stock_num):
    td = TWSE_daily(stock_num, 2010, 1)
    td.start()


def main():
    stocks = ['3535', '2397', '2316', '2392',
              '2888', '3691', '2385', '2337', '3406']
    m = MongodbAPI()

    print("start crawl proxy")
    cp = Crawl_Proxy()
    cp.start()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rDd', [])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)
    opts, args = getopt.getopt(sys.argv[1:], 'rDd')
    for opt, arg in opts:
        if opt in ("-r"):
            # Realtime Parser End
            print("start realtime parser")
            threads = []
            thread_num = len(stocks)
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=twse_realtime, args=(stocks[i],)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                print("Done.")
            # Realtime Parser End
        elif opt == "-D":
            print("start daily parser")
            threads = []
            thread_num = len(stocks)
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=twse_daily, args=(stocks[i],)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                print("Done.")
        elif opt == "-d":
            # 每日交易明細
            print("start daily detail stock")
            threads = []
            thread_num = len(stocks)
            ml = Money_link()
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=money_link, args=(m, ml, stocks[i],)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                print("Done.")
            # 每日交易明細 結束

    close_proxy()


if __name__ == '__main__':
    main()
