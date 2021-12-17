import scrapy


class BabybibiSpider(scrapy.Spider):
    name = 'babybibi'
    allowed_domains = ['babybibi.com']
    start_urls = ['https://babybibi.com/collections/all?page=1/']

    def parse(self, response):
        
        for products in response.xpath("//div[@class='page-width'][@id='Collection']/div/div"):
            yield{
                   'title': products.xpath(".//div[@class='h4 grid-view-item__title']/text()").get(),
                    'original_price': products.xpath(".//s[@class='product-price__price']/text()").get(),
                    'sale_price': products.xpath(".//span[@class='product-price__price product-price__sale']/text()").get()

                }

        next_page = response.urljoin(response.xpath("a[@class='btn btn--secondary btn--narrow']/@href").get())

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
