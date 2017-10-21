# -*- coding: utf-8 -*-
import scrapy
from collectips.items import CollectipsItem


class IpSpiderSpider(scrapy.Spider):
    name = 'ip_spider'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn']

    def start_requests(self):
        reqs = []
        for i in range(1, 206):
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
