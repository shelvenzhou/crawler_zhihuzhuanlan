from scrapy.conf import settings
import pymongo

class MongoHelper:
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        self._columndb = tdb['Column']
        self._postdb = tdb['Post']


    def saveColumn(self, colJson):
        self._columndb.insert(colJson)

    def savePost(self, postJson):
        self._postdb.insert(postJson)

