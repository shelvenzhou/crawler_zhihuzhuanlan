import scrapy
import json
from scrapy.conf import settings
import pymongo
from bs4 import BeautifulSoup
from utils import ZhihuClient,MongoHelper
from utils.common import *

class ZhihuColumnSpider(scrapy.Spider):
        name = "zhihuColumn"
        start_urls = [
                'http://zhuanlan.zhihu.com/api/columns/niceliving',
                                            ]
        # def __init__(self, name=None, **kwargs):
        #     super(zhihuColumnSpider, self).__init__()


        db = MongoHelper()
        #client init
        client = ZhihuClient('cookies.json')

        def parse(self, response):
            colJson = json.loads(response.body)
            self.db.saveColumn(colJson)
            postsCount = colJson[ "postsCount"]
            slug = colJson["slug"]
            self.client._session.headers.update(Host='zhuanlan.zhihu.com')
            for offset in range(0, (postsCount - 1) // 10 + 1):
                posts = self.client._session.get(Column_Posts_Data.format(slug, offset * 10)).json()
                for post in posts:
                    self.db.savePost(post)
            self.client._session.headers.update(Host='www.zhihu.com')
            creator = colJson['creator']['slug']
            creatorUrl = UserColFollowed_URL.format(creator)
            soup = BeautifulSoup(self.client._session.get(creatorUrl).text)
            column_tags = soup.find_all('div', class_='zm-profile-section-item zg-clear')
            if column_tags is None:
                return
            for column_tag in column_tags:
                zhuanlanUrl = column_tag.div.a['href']
                apiUrl = Column_API + '/' + zhuanlanUrl.split('/')[-1]
                yield scrapy.Request(apiUrl, callback=self.parse)