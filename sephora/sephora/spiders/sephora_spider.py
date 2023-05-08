from selenium import webdriver
import scrapy
from scrapy.http import HtmlResponse

class SephoraSpider(scrapy.Spider):
    allowed_domains = ['sephora.com/shop/skincare']
    name = "sephora_spider"
    start_urls = [
        'https://www.sephora.com/shop/skincare'
    ]
    custom_settings = {
        'FEEDS':{
            'sephoradata.json':{'format':'json', 'overwrite':True}
        }
    }
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24'
    ]

    def parse(self, response):
        for products in response.css('div.css-1322gsb'):
            try:
                yield{
                    'name': products.css('span.css-bpsjlq eanm77i0::text').get(), 
                    'description': products.css('span.ProductTile-name.css-h8cc3p.eanm77i0::text').get(),
                    'price': products.css('b.css-1f35s9q::text').get(),
                    'link': products.css('a.css-klx76').attrib['href'],
                }
            except:
                yield{
                    'name': products.css('span.css-bpsjlq eanm77i0::text').get(), 
                    'description': products.css('span.ProductTile-name.css-h8cc3p.eanm77i0::text').get(),
                    'price': products.css('b.css-1f35s9q::text').get(),
                    'link': products.css('a.css-klx76').attrib['href'],
                }
            next_page = response.css('button.css-bk5oor.e65zztl0').attrib['href']
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)  





    # def parse(self, response):
    #     # Extract product links from the category page
    #     for product_link in response.css('.css-ix8km1 ::attr(href)').getall():
    #         yield response.follow(product_link, self.parse_product)

    #     # Follow the "Load More" button if present
    #     next_page = response.css('.css-xb97g1 ::attr(href)').get()
    #     if next_page:
    #         yield response.follow(next_page, self.parse)

    # def parse_product(self, response):
    #     # Extract product information from the product page
    #     yield {
    #         'name': response.css('.css-0 ::text').get(),
    #         'brand': response.css('.css-slwsq8 ::text').get(),
    #         'description': response.css('.css-qbtc43 ::text').get(),
    #         'price': response.css('.css-slwsq8 + .css-11s12ax ::text').get(),
    #         'image_url': response.css('.css-2yrdk3 ::attr(src)').get()
    #     }
