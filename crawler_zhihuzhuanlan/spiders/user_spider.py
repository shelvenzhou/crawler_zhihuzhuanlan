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
                yield scrapy.Request(url, callback=self.parse_user, cookies=self.cookies)

        def parse_user(self, response):
            item = UserItem()
            slug = response.url.split('/')[-1]
            item['id'] = slug

            hash_id = response.xpath('//div[@class="zm-profile-header-op-btns clearfix"]/button/@data-id').extract_first()
            if hash_id:
                item['hash_id'] = hash_id
            else:
                item['hash_id'] = json.loads(response.xpath('//script[@data-name="ga_vars"]/text()').extract_first())['user_hash']

            item['xsrf'] = response.xpath('//input[@name="_xsrf"]/@value').extract_first()

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
                # title = h.xpath('a/@title').extract_first()
                href = h.xpath('a/@href').extract_first()
                # item['skilled_topics'].append((title,href))
                if href:
                    item['skilled_topics'].append(href.split('/')[-1])

            follow = response.xpath('//div[@class="zm-profile-side-following zg-clear"]/a/strong/text()').extract()
            item['followees_num'] = follow[0]
            item['followers_num'] = follow[1]
            item['followees'] = list()

            item['columns_followed_num'] = 0
            item['topics_num'] = 0
            item['columns_followed'] = list()
            item['topics'] = list()
            for r in response.xpath('//div[@class="zm-profile-side-section-title"]/a'):
                if 'columns' in r.xpath('@href').extract_first().encode('utf-8'):
                    item['columns_followed_num'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))
                elif 'topics' in r.xpath('@href').extract_first().encode('utf-8'):
                     item['topics_num'] = filter(str.isdigit,r.xpath('strong/text()').extract_first().encode("utf-8"))

            item['page_viewed'] = response.xpath('//div[@class="zm-side-section-inner"]/span[@class="zg-gray-normal"]/strong/text()').extract_first()
            # print json.dumps(dict(item))
            # yield scrapy.Request(UserColFollowed_URL.format(slug), callback=self.parse_columns_followed,cookies=self.cookies, meta={'item':item,'slug':slug},priority=10)
            p = {"offset":0, "limit":20, "hash_id":item['hash_id']}
            params = {"method":"next", "params":json.dumps(p,separators=(',',':')),'_xsrf':item['xsrf']}
            yield scrapy.http.FormRequest(ProfileFollowedColumnsListV2, formdata = params , method='GET', callback=self.parse_columns_followed,cookies=self.cookies, meta={'item':item,'params':p},priority=10)


        def parse_columns_followed(self, response):
            item = response.meta['item']
            if response.body != '':
                for r in response.xpath('//div[@class="zm-profile-section-item zg-clear"]'):
                    href = r.xpath('a/@href').extract_first()
                    col_slug = href.split('/')[-1]
                    item['columns_followed'].append(col_slug)
                p = response.meta['params']
                p["offset"] = p["offset"]+20 if p["offset"]+20 < item['columns_followed_num'] else item['columns_followed_num']
                params = {"method":"next", "params":json.dumps(p,separators=(',',':')),'_xsrf':item['xsrf']}
                yield scrapy.http.FormRequest(ProfileFollowedColumnsListV2, formdata = params , method='GET', callback=self.parse_columns_followed,cookies=self.cookies, meta={'item':item,'params':p},priority=10)
            else:
                p = {"offset":0, "order_by":"created", "hash_id":item['hash_id']}
                params = {"method":"next", "params":json.dumps(p,separators=(',',':')),'_xsrf':item['xsrf']}
                yield scrapy.http.FormRequest(ProfileFolloweesListV2 , formdata = params , method='GET', callback=self.parse_followees,cookies=self.cookies, meta={'item':item,'params':p},priority=10)              


        def parse_topics(self, response):
            item = response.meta['item']
            for r in response.xpath('//div[@class="zm-profile-section-item zg-clear"]'):
                href = r.xpath('a/@href').extract_first()
                topic_slug = href.split('/')[-1]
                item['topics'].append(topic_slug)
            # yield scrapy.Request(UserFolloweers_URL.format(slug), callback=self.parse_followees,cookies=self.cookies, meta={'item':item, 'slug':slug})
            yield item

        def parse_followees(self, response):
            item = response.meta['item']
            if response.body != '':
                for r in response.xpath('//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]'):
                    href = r.xpath('div[@class="zm-list-content-medium"]/h2/a/@href').extract_first()
                    item['followees'].append(href.split('/')[-1])
                    yield scrapy.Request(href, callback=self.parse_user)
                p = response.meta['params']
                p["offset"] = p["offset"]+20 if p["offset"]+20 < item['followees_num'] else item['followees_num']
                params = {"method":"next", "params":json.dumps(p,separators=(',',':')),'_xsrf':item['xsrf']}
                yield scrapy.http.FormRequest(ProfileFolloweesListV2 , formdata = params , method='GET', callback=self.parse_followees,cookies=self.cookies, meta={'item':item,'params':p},priority=10)              
            else:
                yield scrapy.Request(UserTopics_URL.format(item['id']), callback=self.parse_topics,cookies=self.cookies, meta={'item':item})
   

            # for r in response.xpath('//div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]'):
            #     href = r.xpath('div[@class="zm-list-content-medium"]/h2/a/@href').extract_first()
            #     item['followees'].append(href.split('/')[-1])
            #     yield scrapy.Request(href, callback=self.parse_user)
            # yield item