# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from googleplay.items import GoogleplayItem
# from googleplay.settings import MONGODB
from pymongo import MongoClient

class GoogleplayPipeline(object):

    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://127.0.0.1:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'privacy')

        self.db_client = MongoClient('mongodb://root:root@127.0.0.1:27017')
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()
    def process_item(self, item, spider):
        self.insert_db(item)

        return item
    def insert_db(self, item):
        if isinstance(item, GoogleplayItem):
            item = dict(item)
        self.db.app.insert_one(item)


    # def __init__(self):
    #     self._db = MONGODB.get('db')
    #     self._collection = MONGODB.get('collection')
    #     self._host = MONGODB.get('host')
    #     self._port = MONGODB.get('port')
    #     self._client = pymongo \
    #         .MongoClient(host=self._host, port=self._port) \
    #         .get_database(self._db) \
    #         .get_collection(self._collection)

    # def process_item(self, item, spider):
    #     self._client.create_index([('id', pymongo.DESCENDING)], background=True)
    #     self._client.update_one(filter={'app_id': item['app_id']}, update={'$set': dict(item)}, upsert=True)
    #     # self._client.save(dict(item))
    #     return item
