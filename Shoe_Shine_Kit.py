import scrapy


class ShoeShineKitSpider(scrapy.Spider):
    name = 'Shoe_Shine_Kit'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=shoe+shine+kit/']

    def parse(self, response):
        for items in response.css('.s-search-results'):
            yield{
                'Title': items.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "a-size-base-plus", " " ))]/text()').extract()
            }
