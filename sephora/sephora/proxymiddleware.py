from scrapy import signals
from scrapy.exceptions import NotConfigured
import random

class ProxyMiddleware(object):
    def __init__(self, proxies):
        self.proxies = proxies

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxies=crawler.settings.getlist('PROXIES')
        )

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxies[0]
