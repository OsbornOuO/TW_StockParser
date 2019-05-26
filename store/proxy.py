from .mongo import MongodbAPI
from random import choice
from datetime import datetime
import threading
import logging

_proxylist = []
lock = threading.RLock()


def init():
    m = MongodbAPI()
    global _proxylist
    for _ in range(5):
        try:
            _proxylist = m.Get_Data_From(
                'proxy', {'_id': 0})["iptable"]
            break
        except Exception as e:
            logging.warn("get proxy error:%s" % (e))
            continue
    else:
        logging.error("Get Proxy list from mongo fail")


def get_proxy() -> dict:
    global _proxylist
    global lock
    lock.acquire()
    if len(_proxylist) != 0:
        tmp = choice(_proxylist)
        lock.release()
        return tmp
    else:
        logging.warn("Start to use local ip")
        lock.release()
        return {}


def delete_proxy(proxy) -> bool:
    global _proxylist
    global lock
    if proxy in _proxylist:
        lock.acquire()
        _proxylist.remove(proxy)
        lock.release()
        return True


def close_proxy():
    m = MongodbAPI()
    global _proxylist
    logging.info("Update proxy list to mongo , length :%d" % (len(_proxylist)))
    m.Update_One('proxy', {
        'id': 0
    }, {
        '$set': {
            'iptable': _proxylist
        }
    })


init()
