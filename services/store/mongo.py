# coding=utf-8

from pymongo import MongoClient

class MongodbAPI(object):
    def __init__(self):
        connection =  MongoClient("mongodb://python-stock:bNMbTAddsZEwpVRI@amazondata-shard-00-00-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-01-7op9t.gcp.mongodb.net:27017,amazondata-shard-00-02-7op9t.gcp.mongodb.net:27017/TWStock?ssl=true&replicaSet=AmazonData-shard-0&authSource=admin")
        db = connection['TWStock']
        self.proxy_collection = db.proxy
    def Get_Data_From(self,collection_name,tag):
        if collection_name is "proxy":
            return self.proxy_collection.find_one(tag)
    def Insert_Data_To(self,collection_name,data):
        if collection_name is "proxy":
            self.proxy_collection.insert_one(data)
    def Insert_Many_Data_To(self,collection_name,data):
        if collection_name is "proxy":
            self.proxy_collection.insert_many(data)
        pass
    def DropAll(self,collection_name):
        if collection_name is "proxy":
            self.proxy_collection.drop()
    def Delete_One(self,collection_name,key,value):
        if collection_name is "proxy":
            self.proxy_collection.delete_one({key:value})
        pass
    def Update_One(self,collection_name,key,value):
        if collection_name is "proxy":
            self.proxy_collection.update_one(key,value)
        pass