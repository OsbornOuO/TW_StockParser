# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_twse import parserTWStock
from services.store.mongo import MongodbAPI
from services.store.proxy import ProxyProvider
from services.crawl_money_link import Money_link


import sys
import getopt


def main():
    m = MongodbAPI()

    print("Start crawl proxy")
    cp = Crawl_Proxy()
    cp.Start()

    # s = parserTWStock('3535', _proxylist)
    # s = parserTWStock('3535', None)
    # print("Start crawl realtime")
    # r = s.get_realtime()
    # print("Start crawl oldprice")
    # o = s.get_oldprice()
    # if r != None:
    #     print("Insert realtime data ")
    #     m.Insert_Data_To("Realtime_data", r)
    # if len(o) != 0:
    #     print("Insert daily data, count: %d" % (len(o)))
    #     m.Insert_Many_Data_To("Daily_data", o)

    print("Start daily detail stock")
    ml = Money_link().Start(3535)
    if len(ml) is not 0:
        print("Insert daily detail stock , count : %d" % (len(ml)))
        m.Insert_Many_Data_To("Transaction_details", ml)

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
