from selenium import webdriver
import scrapy
from scrapy.http import HtmlResponse

class SephoraSpider(scrapy.Spider):
    allowed_domains = ['playwright.dev/']
    name = "sephora_spider"
    start_urls = [
        'https://playwright.dev/'
    ]
    custom_settings = {
        'FEEDS':{
            'sephoradata.json':{'format':'json', 'overwrite':True}
        }
    }

    def parse(self, response):

        products = response.css('div.css-1322gsb')

        for product in products:
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

            next_page = response.css('button.css-bk5oor.e65zztl0').attrib['href'].get()

            if next_page is not None:
                next_page = 'https://www.sephora.com/shop/skincare' + next_page
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
