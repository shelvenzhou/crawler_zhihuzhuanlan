# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ColumnItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    followersCount = scrapy.Field()
    postsCount = scrapy.Field()
    name = scrapy.Field()
    slug = scrapy.Field()
    pass

class UserItem(scrapy.Item):
    id = scrapy.Field()
    agree = scrapy.Field()
    thanks = scrapy.Field()
    asks = scrapy.Field()
    answers = scrapy.Field()
    posts = scrapy.Field()
    collections = scrapy.Field()
    logs = scrapy.Field()
    skilled_topics = scrapy.Field()
    followees = scrapy.Field()
    followers = scrapy.Field()
    columns_followed = scrapy.Field()
    topics = scrapy.Field()
    page_viewed = scrapy.Field()


