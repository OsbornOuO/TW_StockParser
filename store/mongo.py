# -*- coding: utf-8 -*-

from pymongo import MongoClient, errors
import logging

MONGOCONNECTIONSTR = "mongodb://python-stock:bNMbTAddsZEwpVRI@amazondata-shard-00-00-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-01-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-02-7op9t.gcp.mongodb.net:27017/TWStock?ssl=true&replicaSet=AmazonData-shard-0&authSource=admin"
# MONGOCONNECTIONSTR = "mongodb://chenzhaohui.asuscomm.com:27017/TWStock&authSource=admin"


class MongodbAPI(object):
    def __init__(self):
        connection = MongoClient(
            MONGOCONNECTIONSTR, maxPoolSize=30, waitQueueMultiple=20, waitQueueTimeoutMS=1000)
        self.db = connection['TWStock']

    def Get_Data_From(self, collection_name, tag):
        return self.db[collection_name].find_one(tag)

    def Insert_Data_To(self, collection_name, data) -> bool:
        try:
            self.db[collection_name].insert_one(data)
        except:
            logging.info("_id exists")
            return False

    def Insert_Many_Data_To(self, collection_name, data) -> bool:
        try:
            self.db[collection_name].insert_many(data)
            return True
        except Exception as e:
            logging.error(
                "Insert Many data to mongo, error : %s" % (e.args[0]))
            return False

    def DropAll(self, collection_name):
        self.db[collection_name].drop()

    def Delete_One(self, collection_name, key, value):
        self.db[collection_name].drop({key: value})

    def Update_One(self, collection_name, key, value):
        """Update_One provide update"""
        self.db[collection_name].update(key, value, upsert=False)

    def Upsert(self, collection_name, key, value):
        """Upsert provide upsert"""
        self.db[collection_name].update(key, value, upsert=True)

    def CheckExists(self, collection_name, value) -> bool:
        """CheckExists provide check if '_id' exists"""
        if len(list(self.db[collection_name].find({'_id': value}).limit(1))):
            return True
        else:
            return False
