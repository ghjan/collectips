# -*- coding: utf-8 -*-
import scrapy


class IpSpiderSpider(scrapy.Spider):
    name = 'ip_spider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        pass
