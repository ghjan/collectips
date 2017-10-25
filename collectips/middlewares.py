# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class CollectipsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random
from collectips.settings import IPPOOL_HTTP, IPPOOL_HTTPS
from collectips.ipadd import IPPOOL_BACKUP_HTTP, IPPOOL_BACKUP_HTTPS
from collectips.utils.dbhelper import DBHelp


class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        print("type of request:{}".format(request))
        # Set the location of the proxy
        if IPPOOL_HTTP is None:
            sql = "select ip, port, `type` from ips"
            DBHelp().query(sql, self.after_queryips, request=request)
        else:
            self.after_queryips(None, request=request)

    def after_queryips(self, rs, request=None):
        from collectips.settings import IPPOOL_HTTP, IPPOOL_HTTPS
        if rs:
            if IPPOOL_HTTP is None:
                IPPOOL_HTTP = []
            if IPPOOL_HTTPS is None:
                IPPOOL_HTTPS = []
            for r in rs:
                try:
                    url_ = r['type'].decode('utf-8') + '//' + r['ip'].decode('utf-8') + ':' + r['port'].decode('utf-8')
                    IPPOOL_HTTP.append(url_) if r['type'].strip() == 'HTTP' else IPPOOL_HTTPS.append(url_)
                except Exception as e:
                    print("r:{}".format(r))
                    print(e)
        thisip = self._get_address(request['request'])
        print("this is ip:" + thisip)
        if request:
            request['request'].meta["proxy"] = thisip
        else:
            print("Exception, request is None?!!!")

    def _get_address(self, request):
        is_http = request.url.startswith("http://")
        ippool_backup = IPPOOL_BACKUP_HTTP if is_http else IPPOOL_BACKUP_HTTPS
        ippool = IPPOOL_HTTP if is_http else IPPOOL_HTTPS
        use_backup = not IPPOOL_HTTP if is_http else not IPPOOL_HTTPS
        thisip = 'http://' + random.choice(ippool_backup) if use_backup else random.choice(ippool)
        return thisip
