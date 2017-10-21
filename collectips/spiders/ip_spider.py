# -*- coding: utf-8 -*-
import scrapy
from collectips.items import CollectipsItem


class IpSpiderSpider(scrapy.Spider):
    name = 'ip_spider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn']

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

    def start_requests(self):
        reqs = []
        for i in range(1, 3):
            req = scrapy.Request("http://www.xicidaili.com/nn/{}".format(i))
            reqs.append(req)
        return reqs

    def parse(self, response):
        ip_list = response.xpath('//table[@id="ip_list"]/tbody')
        trs = ip_list.xpath('tr')
        items = []
        for tr in trs:
            item = CollectipsItem()
            item['IP'] = tr.xpath('td[2]/text()').extract_first()
            item['PORT'] = tr.xpath('td[3]/text()').extract_first()
            item['POSITION'] = tr.xpath('td[4]/text()').extract_first()
            item['TYPE'] = tr.xpath('td[6]/text()').extract_first()
            item['SPEED'] = tr.xpath('td[7]/div/@title').re_first('\d{0,2}\.\d{0,}')
            item['LAST_CHECK_TIME'] = tr.xpath('td[10]/text()').extract_first()
            items.append(item)
        return items
