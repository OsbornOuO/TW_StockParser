# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_money_link import Money_link
from services.crawl_twse_realtime import TWSE_realtime
from services.crawl_twse_daily import TWSE_daily
from store.proxy import close_proxy
from store.mongo import MongodbAPI

import sys
import getopt
import threading
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)-7s : %(message)s', level=logging.INFO)


def money_link(m, ml, stock: list):
    logging.info("start to parser stock : %s" % (stock))
    data = ml.start(stock)
    if len(data) is not 0:
        logging.info("Insert daily detail stock:%s, count : %d" %
                     (stock, len(data)))
        m.Insert_Many_Data_To("Transaction_details", data)


def twse_realtime(stock_num):
    logging.info("start to parser stock : %s" % (stock_num))
    tr = TWSE_realtime(stock_num)
    tr.start()


def twse_daily(stock_num, year, month):
    td = TWSE_daily(stock_num, year, month)
    td.start()


def main():
    stocks = ['3455', '5443', '8064', '2409', '1504',
              '3535', '2397', '2316', '2392', '2888',
              '2385', '2337', '3406', '2492',
              '2478', '6182', '8163', '2337', '2481',
              '3016', '6153', '3630', '4190']
    m = MongodbAPI()

    cp = Crawl_Proxy()
    cp.start()

    opts, args = [], []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'rDd', [])
    except getopt.GetoptError as err:
        logging.error(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-r"):
            # Realtime Parser End
            logging.info("start realtime parser")
            threads = []
            thread_num = len(stocks)
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=twse_realtime, args=(stocks[i],)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                logging.info("Thread Done")
            # Realtime Parser End
        elif opt == "-D":
            logging.info("start daily parser")
            threads = []
            thread_num = len(stocks)
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=twse_daily, args=(stocks[i], 2007, 1)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                logging.info("Thread Done")
        elif opt == "-d":
            # 每日交易明細
            logging.info("start daily detail stock")
            threads = []
            thread_num = len(stocks)
            ml = Money_link()
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=money_link, args=(m, ml, stocks[i],)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                logging.info("Thread Done")
            # 每日交易明細 結束

    close_proxy()


if __name__ == '__main__':
    main()
