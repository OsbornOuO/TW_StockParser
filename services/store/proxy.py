from .mongo import MongodbAPI
from random import choice


class ProxyProvider():
    def __init__(self):
        self.__proxylist = []
        self.__getProxy()
        self.__health = True

    def __getProxy(self):
        m = MongodbAPI()

        for _ in range(5):
            try:
                proxy = m.Get_Data_From('proxy', {'id': 0})
                self.__proxylist = [{'http': x} for x in proxy['ip']]
                break
            except Exception as e:
                print(e)
                continue
        else:
            self.health = False
            print("Get Proxy list from mongo fail")
        print(self.__proxylist)
    def get_proxies(self):
        if self.__health:
            return choice(self.__proxylist)
        else:
            None
