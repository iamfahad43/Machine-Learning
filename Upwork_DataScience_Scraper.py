import scrapy


class UpworkDatascienceScraperSpider(scrapy.Spider):
    name = 'Upwork_DataScience_Scraper'
    allowed_domains = ['www.upwork.com']
    start_urls = ['https://www.upwork.com/search/profiles/?q=data%20science~']

    def parse(self, response):
        for scientist in response.xpath("//div[@class='up-card-section up-card-hover']"):
            yield {
                    'Name': scientist.xpath(".//div[@class='identity-name']/text()").get(),
                    'Title': scientist.xpath(".//p[@class='my-0 freelancer-title']/strong/text()").get(),
                    'Hourly_Rate': scientist.xpath(".//div[@class='grid-col-1 grid-col-sm-1 justify-self-start nowrap']/strong/span/text()").get(),
                    'Skills': scientist.xpath(".//div[@class='up-skill-wrapper']").get(),
                    'Discription': scientist.xpath(".//div[@class='up-line-clamp-v2 clamped']/text()").get()
                }
