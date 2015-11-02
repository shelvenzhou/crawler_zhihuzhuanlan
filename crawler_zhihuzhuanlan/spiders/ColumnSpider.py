# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

email = 'zhuanlan_test@sina.com'
passwd = 'zhihutest'

# store all visited users in case of duplication
users = []


class ColumnSpider(scrapy.Spider):
	name = 'ColumnSpider'
	allowed_domains = ['zhihu.com']
	start_urls = [
		'http://www.zhihu.com',
	]

	def parse(self, response):
		xsrf = Selector(response).xpath('//input[@name="_xsrf"]/@value').extract()[0]

		# get captcha
		return scrapy.Request(
			url='http://www.zhihu.com/captcha.gif',
			meta={'_xsrf': xsrf},
			callback=self.login
		)

	def login(self, response):
		f = open('captcha.gif', 'w+')
		for line in response.body:
			f.write(line)
		f.close()

		print 'Please input captcha:'
		captcha_str = raw_input()

		# TODO: read account info from file

		# login
		return [scrapy.FormRequest(
			'http://www.zhihu.com/login/email',
			formdata={
				'_xsrf': response.meta['_xsrf'],
				'email': email,
				'password': passwd,
				'remember_me': 'true',
				'captcha': captcha_str,
			},
			callback=self.after_login
		)]

	def after_login(self, response):
		if "\"r\": 1" in response.body:
			self.logger.error('Login Failed')
			return

		self.logger.debug('Login Succeed')

		# use a popular person as entry
		return scrapy.Request(
			url='http://www.zhihu.com/people/xiepanda/followers',
			meta={'username': 'xiepanda'},
			callback=self.parse_followers
		)

	def parse_followers(self, response):
		yield scrapy.Request(
			url='http://www.zhihu.com/people/%s/columns/followed' % response.meta['username'],
			callback=self.parse_columns
		)

		return

	def parse_columns(self, response):


		return
