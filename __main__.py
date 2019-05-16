# -*- coding: utf-8 -*-
from services.crawl_proxy import Crawl_Proxy
from services.crawl_twse import parserTWStock
from services.store.mongo import MongodbAPI

def main():
    cp = Crawl_Proxy(
        "http://www.cybersyndrome.net/search.cgi?q=&a=ABCD&f=s&s=new&n=500")
    cp.Start()

    m = MongodbAPI()
    proxy = m.Get_Data_From('proxy', {'id': 0})
    _proxylist = [{'http': x} for x in proxy['ip']]
    s = parserTWStock('3535', _proxylist)
    r = s.get_realtime()
    o = s.get_oldprice()
    print(r)
    print(o)
    m.Insert_Data_To("Realtime_data",r)
    m.Insert_Many_Data_To("Daily_data",o)

if __name__ == '__main__':
    main()
