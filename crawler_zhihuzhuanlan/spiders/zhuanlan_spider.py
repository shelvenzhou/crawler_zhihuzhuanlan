import scrapy
import json
from scrapy.conf import settings
import pymongo
from bs4 import BeautifulSoup
from columns import ZhihuClient
# from crawler_zhihuzhuanlan.items import ColumnItem

class ZhihuColumnSpider(scrapy.Spider):
        name = "zhihuColumn"
        start_urls = [
                'http://zhuanlan.zhihu.com/api/columns/niceliving',
                                            ]
        # def __init__(self, name=None, **kwargs):
        #     super(zhihuColumnSpider, self).__init__()

        #mongodb init
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[dbName]
        post = tdb[settings['MONGODB_DOCNAME']]

        #client init
        client = ZhihuClient('cookies.json')

        def parse(self, response):
            colJson = json.loads(response.body)
            self.post.insert(colJson)
            # item = ColumnItem()
            # item['followersCount'] = colJson['followersCount']
            # item['name'] = colJson['name']
            # item['postsCount'] = colJson['postsCount']
            # item['slug'] = colJson['slug']
            # yield item
            print colJson['slug']
            creator = colJson['creator']['slug']
            creatorUrl = 'http://www.zhihu.com/people/' + creator + '/columns/followed'
            soup = BeautifulSoup(self.client._session.get(creatorUrl).text)
            column_tags = soup.find_all('div', class_='zm-profile-section-item zg-clear')
            if column_tags is None:
                return
            for column_tag in column_tags:
                zhuanlanUrl = column_tag.div.a['href']
                apiUrl = 'http://zhuanlan.zhihu.com/api/columns/' + zhuanlanUrl.split('/')[-1]
                yield scrapy.Request(apiUrl, callback=self.parse)