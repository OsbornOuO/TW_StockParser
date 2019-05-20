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
                self.__proxylist = m.Get_Data_From(
                    'proxy', {'id': 0})["iptable"]
                break
            except Exception as e:
                continue
        else:
            self.__health = False
            print("Get Proxy list from mongo fail")

    def get_proxy(self):
        if len(self.__proxylist) != 0:
            return choice(self.__proxylist)
        else:
            None
