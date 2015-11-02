import scrapy
from scrapy.conf import settings
import json

from utils import ZhihuClient
from utils.common import *

from crawler_zhihuzhuanlan.items import UserItem

class ZhihuUserSpider(scrapy.Spider):
        name = "zhihuUser"
        start_urls = [
                'http://www.zhihu.com/explore',
                                            ]
        cookies = json.loads(settings['COOKIES'])

        def parse(self, response):
            for href in response.xpath('//h3[@class="zm-item-answer-author-wrap"]/a/@href'):
                # print href.extract()
                url =  response.urljoin(Zhihu_URL + href.extract())
                yield scrapy.Request(url, callback=self.parse_user)

        def parse_user(self, response):
            slug = response.url.split('/')[-1]
            # print UserFolloweers_URL.format(slug)
            yield scrapy.Request(UserFolloweers_URL.format(slug), callback=self.parse_followees,cookies=self.cookies)           
            item = UserItem()
            item['id'] = slug
            item['agree'] =  response.xpath('//span[@class="zm-profile-header-user-agree"]/strong/text()').extract_first()
            item['thanks'] = response.xpath('//span[@class="zm-profile-header-user-thanks"]/strong/text()').extract_first()

            profile = response.xpath('//div[@class="profile-navbar clearfix"]/a[@class="item "]/span/text()').extract()
            item['asks'] = profile[0]
            item['answers'] = profile[1]
            item['posts'] = profile[2]
            item['collections'] = profile[3]
            item['logs'] = profile[4]

            item['skilled_topics'] = list()
            for h in response.xpath('//div[@class="zm-profile-section-list zg-clear"]/div'):
                title = h.xpath('a/@title').extract_first()
                href = h.xpath('a/@href').extract_first().split('/')[-1]
                # item['skilled_topics'].append((title,href))
                item['skilled_topics'].append(href)

            follow = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a/strong/text()').extract()
            item['followees'] = follow[0]
            item['followers'] = follow[1]

            for r in response.xpath('//div[@class="zm-profile-side-section-title"]/a'):
                if 'columns' in r.xpath('@href').extract_first().encode('utf-8'):
                    item['columns_followed_num'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))
                elif 'topics' in r.xpath('@href').extract_first().encode('utf-8'):
                     item['topics_num'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))

            item['page_viewed'] = response.xpath('//div[@class="zm-side-section-inner"]/span[@class="zg-gray-normal"]/strong/text()').extract_first()
            # print json.dumps(dict(item))
            yield scrapy.Request(UserColFollowed_URL.format(slug), callback=self.parse_columns_followed,cookies=self.cookies, meta={'item':item,'slug':slug},priority=10)


        def parse_followees(self, response):
            # print "parse_followees: " + response.url
            for r in response.xpath('//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]'):
                href = r.xpath('div[@class="zm-list-content-medium"]/h2/a/@href').extract_first()
                # print "\nhref: " + href
                yield scrapy.Request(href, callback=self.parse_user)

        def parse_columns_followed(self, response):
            slug = response.meta['slug']
            item = response.meta['item']
            item['columns_followed'] = list()
            for r in response.xpath('//div[@class="zm-profile-section-item zg-clear"]'):
                href = r.xpath('a/@href').extract_first()
                col_slug = href.split('/')[-1]
                item['columns_followed'].append(col_slug)
            # yield scrapy.Request(UserTopics_URL.format(slug), callback=self.parse_topics,cookies=self.cookies, meta={'item':item},priority=20)
            yield item

        # def parse_topics(self, response):
        #     item = response.meta['item']
        #     item['topics'] = list()
        #     for r in response.xpath('//div[@class="zm-profile-section-item zg-clear"]'):
        #         href = r.xpath('a/@href').extract_first()
        #         slug = href.split('/')[-1]
        #         item['topics'].append(slug)
        #     yield item

