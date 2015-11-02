from scrapy.conf import settings
import pymongo
import json
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class UserDBPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self._userdb = tdb['User']

    def process_item(self, item, spider):
        itemInfo = dict(item)
        self._userdb.insert(itemInfo)
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('users.txt', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item