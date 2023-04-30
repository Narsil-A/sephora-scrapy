import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

driver = webdriver.Chrome(executable_path='C:\Users\Narsil\dev\seleniumDrivers')

class SephoraSkincareSpider(scrapy.Spider):
    name = "sephora_skincare"
    start_urls = [
        'https://www.sephora.com/shop/skincare'
    ]
    def start_requests(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.example.com')
        body = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=body, encoding='utf-8')
        yield scrapy.Request(url=response.url, callback=self.parse)

    def parse(self, response):
        # Extract product links from the category page
        for product_link in response.css('.css-klx76 ::attr(href)').getall():
            yield response.follow(product_link, self.parse_product)

        # Follow the "Load More" button if present
        next_page = response.css('.css-xb97g1 ::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        # Extract product information from the product page
        yield {
            'name': response.css('.css-0 ::text').get(),
            'brand': response.css('.css-slwsq8 ::text').get(),
            'description': response.css('.css-qbtc43 ::text').get(),
            'price': response.css('.css-slwsq8 + .css-11s12ax ::text').get(),
            'image_url': response.css('.css-2yrdk3 ::attr(src)').get()
        }