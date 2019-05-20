# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_twse import parserTWStock
from services.store.mongo import MongodbAPI
from services.crawl_money_link import Money_link
from services.crawl_twse_realtime import TWSE_realtime

import sys
import getopt
import threading


def money_link(m, ml, stock: str):
    print("start to parser stock :", stock)
    data = ml.start(stock)
    if len(data) is not 0:
        print("Insert daily detail stock:%s, count : %d" % (stock, len(data)))
        m.Insert_Many_Data_To("Transaction_details", data)


def main():
    # stocks = ['3535', '2397', '2316', '2392',
    #           '2888', '3691', '2385', '2337', '3406']
    # m = MongodbAPI()

    # print("start crawl proxy")
    # cp = Crawl_Proxy()
    # cp.start()

    tr = TWSE_realtime(3535)
    tr.start()
    # s = parserTWStock('3535', _proxylist)
    # s = parserTWStock('3535', None)
    # print("start crawl realtime")
    # r = s.get_realtime()
    # print("start crawl oldprice")
    # o = s.get_oldprice()
    # if r != None:
    #     print("Insert realtime data ")
    #     m.Insert_Data_To("Realtime_data", r)
    # if len(o) != 0:
    #     print("Insert daily data, count: %d" % (len(o)))
    #     m.Insert_Many_Data_To("Daily_data", o)

    # 每日交易明細
    # print("start daily detail stock")
    # threads = []
    # thread_num = len(stocks)
    # ml = Money_link()
    # for i in range(thread_num):
    #     threads.append(threading.Thread(
    #         target=money_link, args=(m, ml, stocks[i],)))
    #     threads[i].start()
    # for i in range(thread_num):
    #     threads[i].join()
    #     print("Done.")
    # 每日交易明細 結束

    # try:
    #     opts, args = getopt.getopt(sys.argv[1:], 'stwa', [])
    # except getopt.GetoptError as err:
    #     print(str(err))
    #     sys.exit(2)
    # opts, args = getopt.getopt(sys.argv[1:], 'stwa')
    # for opt, arg in opts:
    #     if opt in ("-s"):
    #         pass
    #     elif opt == "-t":
    #         pass


if __name__ == '__main__':
    main()
