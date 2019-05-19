# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_twse import parserTWStock
from services.store.mongo import MongodbAPI
from services.crawl_money_link import Money_link


def main():
    m = MongodbAPI()

    print("Start crawl proxy")
    cp = Crawl_Proxy(
        "http://www.cybersyndrome.net/search.cgi?q=&a=ABCD&f=s&s=new&n=500")
    cp.Start()   

    proxy = m.Get_Data_From('proxy', {'id': 0})
    _proxylist = [{'http': x} for x in proxy['ip']]

    s = parserTWStock('3535', _proxylist)  
    print("Start crawl realtime")
    r = s.get_realtime()
    print("Start crawl oldprice")
    o = s.get_oldprice()
    if r != None:
        m.Insert_Data_To("Realtime_data", r)
    if len(o) != 0:
        m.Insert_Many_Data_To("Daily_data", o)

    print("Start  daily detail stock")
    ml = Money_link()
    m.Insert_Many_Data_To("Transaction_details", ml.Start(3535))


if __name__ == '__main__':
    main()
