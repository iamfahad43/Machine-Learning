import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlShoeShineSpider(CrawlSpider):
    name = 'Crawl_Shoe_Shine'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=shoe+shine+kit/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='a-link-normal a-text-normal']"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #print(response)
        yield{
            'Title': response.xpath("//span[@class='a-size-large product-title-word-break']/text()").get()
            #'Rating': response.xpath("((//span[@id='acrCustomerReviewText'])[1])/text()").get()
            #'Store': response.xpath("//a[@id='bylineInfo']/text()").get()
        }
        #item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        #return item
