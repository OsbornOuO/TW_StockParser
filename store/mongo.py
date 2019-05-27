# -*- coding: utf-8 -*-

from pymongo import MongoClient, errors
import logging

MONGOCONNECTIONSTR = "mongodb://python-stock:bNMbTAddsZEwpVRI@amazondata-shard-00-00-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-01-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-02-7op9t.gcp.mongodb.net:27017/TWStock?ssl=true&replicaSet=AmazonData-shard-0&authSource=admin"
# MONGOCONNECTIONSTR = "mongodb://chenzhaohui.asuscomm.com:27017/TWStock&authSource=admin"


class MongodbAPI(object):
    def __init__(self):
        connection = MongoClient(
            MONGOCONNECTIONSTR, maxPoolSize=100, waitQueueMultiple=50, waitQueueTimeoutMS=1000)
        db = connection['TWStock']
        self.proxy_collection = db.proxy
        self.realtime = db.Realtime_data
        self.daily = db.Daily_data
        self.Transaction_details = db.Transaction_details
        self.stock_information = db.stock_information
        self.stock_daily_info = db.stock_daily_info

    def Get_Data_From(self, collection_name, tag):
        if collection_name is "proxy":
            return self.proxy_collection.find_one(tag)

    def Insert_Data_To(self, collection_name, data) -> bool:
        if collection_name is "proxy":
            try:
                self.proxy_collection.insert_one(data)
                return True
            except:
                logging.info("_id exists")
                return False
        elif collection_name is "Realtime_data":
            try:
                self.realtime.insert_one(data)
                return True
            except errors.DuplicateKeyError:
                logging.info("_id exists")
                return False
        elif collection_name is "Daily_data":
            try:
                self.daily.insert_one(data)
                return True
            except errors.DuplicateKeyError:
                logging.info("_id exists")
                return False
        elif collection_name is "Transaction_details":
            try:
                self.Transaction_details.insert_one(data)
                return True
            except errors.DuplicateKeyError:
                logging.info("_id exists")
                return False
        return False

    def Insert_Many_Data_To(self, collection_name, data) -> bool:
        if collection_name is "proxy":
            try:
                self.proxy_collection.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False
        elif collection_name is "Realtime_data":
            try:
                self.realtime.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False
        elif collection_name is "Daily_data":
            try:
                self.daily.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False
        elif collection_name is "Transaction_details":
            try:
                self.Transaction_details.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False
        elif collection_name is "stock_information":
            try:
                self.stock_information.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False
        elif collection_name is "stock_daily_info":
            try:
                self.stock_daily_info.insert_many(data)
                return True
            except Exception as e:
                logging.error(
                    "Insert Many data to mongo, error : %s" % (e.args[0]))
                return False

    def DropAll(self, collection_name):
        if collection_name is "proxy":
            self.proxy_collection.drop()

    def Delete_One(self, collection_name, key, value):
        if collection_name is "proxy":
            self.proxy_collection.delete_one({key: value})
        pass

    def Update_One(self, collection_name, key, value):
        """Update_One provide update"""
        if collection_name is "proxy":
            self.proxy_collection.update(key, value, upsert=False)
        pass

    def Upsert(self, collection_name, key, value):
        """Upsert provide upsert"""
        if collection_name is "proxy":
            self.proxy_collection.update(key, value, upsert=True)
        pass

    def CheckExists(self, collection_name, value) -> bool:
        """CheckExists provide check if '_id' exists"""
        if collection_name is "Realtime_data":
            if len(list(self.realtime.find({'_id': value}).limit(1))):
                return True
            else:
                return False
        elif collection_name is "Daily_data":
            if len(list(self.daily.find({'_id': value}).limit(1))):
                return True
            else:
                return False
        elif collection_name is "Transaction_details":
            if len(list(self.Transaction_details.find({'_id': value}).limit(1))):
                return True
            else:
                return False
