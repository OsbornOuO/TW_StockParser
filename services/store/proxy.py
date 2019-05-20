from .mongo import MongodbAPI
from random import choice

_proxylist = []


def init():
    m = MongodbAPI()
    global _proxylist
    for _ in range(5):
        try:
            _proxylist = m.Get_Data_From(
                'proxy', {'id': 0})["iptable"]
            break
        except Exception as e:
            continue
    else:
        print("Get Proxy list from mongo fail")


def get_proxy() -> dict:
    global _proxylist
    if len(_proxylist) != 0:
        return choice(_proxylist)
    else:
        return {}


init()
