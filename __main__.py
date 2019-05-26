# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_money_link import Money_link
from services.crawl_twse_realtime import TWSE_realtime
from services.crawl_twse_daily import TWSE_daily
from services.crawl_Institutional_investors import Institutional_investors
from store.proxy import close_proxy
from store.mongo import MongodbAPI

import sys
import getopt
import threading
import logging
import random
from datetime import datetime
from datetime import timedelta

logging.basicConfig(
    format='%(asctime)s - %(levelname)-7s : %(message)s', level=logging.INFO)


def money_link(m, ml, stock: list):
    logging.info("start to parser stock : %s" % (stock))
    data = ml.start(stock)
    if len(data) is not 0:
        for i in range(5):
            err = m.Insert_Many_Data_To("Transaction_details", data)
            if err:
                logging.info("Insert daily detail stock:%s, count : %d" %
                             (stock, len(data)))
                break
            else:
                logging.warning(
                    "Fail to Insert daily detail stock:%s , retry :%d" % (stock, i+1))


def twse_realtime(stock_num):
    logging.info("start to parser stock : %s" % (stock_num))
    tr = TWSE_realtime(stock_num)
    tr.start()


def twse_daily(stock_num, year, month):
    td = TWSE_daily(stock_num, year, month)
    td.start()


def tse_institutional_investors(date_list):
    global lock

    while True:
        lock.acquire()
        length = len(date_list)
        if length <= 0:
            lock.release()
            break
        tmp_date = date_list.pop()
        lock.release()
        lp = Institutional_investors(tmp_date)
        lp.start()


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
        opts, args = getopt.getopt(sys.argv[1:], 'rDdi', [])
    except getopt.GetoptError as err:
        logging.error(err)
        sys.exit(2)
    for opt, args in opts:
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
        elif opt == "-i":
            # 產生 從 2010/1/1 -> now
            date_list = []
            start_at = datetime(2012, 5, 2)
            # end_at = datetime(2018, 12, 31)
            end_at = datetime.now()
            step = timedelta(days=1)
            while start_at <= end_at:
                date_list.append(start_at.date())
                start_at += step
            random.shuffle(date_list)

            threads = []
            thread_num = 16
            for i in range(thread_num):
                threads.append(threading.Thread(
                    target=tse_institutional_investors, args=(date_list,)))
                threads[i].start()
            for i in range(thread_num):
                threads[i].join()
                logging.info("Thread Done")
    else:
        close_proxy()


if __name__ == '__main__':
    lock = threading.Lock()

    main()
