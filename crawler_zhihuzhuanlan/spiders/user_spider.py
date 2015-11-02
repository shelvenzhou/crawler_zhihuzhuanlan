import scrapy
import json

from utils import ZhihuClient
from utils.common import *

from crawler_zhihuzhuanlan.items import UserItem

class ZhihuUserSpider(scrapy.Spider):
        name = "zhihuUser"
        start_urls = [
                'http://www.zhihu.com/explore',
                                            ]
        cookies = json.loads(COOKIES)

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
                href = h.xpath('a/@href').extract_first()
                # item['skilled_topics'].append((title,href))
                item['skilled_topics'].append(href)

            follow = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a/strong/text()').extract()
            item['followees'] = follow[0]
            item['followers'] = follow[1]

            for r in response.xpath('//div[@class="zm-profile-side-section-title"]/a'):
                if 'columns' in r.xpath('@href').extract_first().encode('utf-8'):
                    item['columns_followed'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))
                elif 'topics' in r.xpath('@href').extract_first().encode('utf-8'):
                     item['topics'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))

            item['page_viewed'] = response.xpath('//div[@class="zm-side-section-inner"]/span[@class="zg-gray-normal"]/strong/text()').extract_first()
            # print json.dumps(dict(item))
            yield item


        def parse_followees(self, response):
            # print "parse_followees: " + response.url
            for r in response.xpath('//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]'):
                href = r.xpath('div[@class="zm-list-content-medium"]/h2/a/@href').extract_first()
                print "\nhref: " + href
                yield scrapy.Request(href, callback=self.parse_user)