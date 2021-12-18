import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield{
                'Title': response.xpath("//div[@class='TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt']/h1/text()").get(),
                'Released_Date': response.xpath("(//span[@class='TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex']/text())[1]").get(),
                'Duration_in_hours': response.xpath("//li[@class='ipc-inline-list__item']/text()").get(),
                'Rating': response.xpath("(//span[@class='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV']/text())[2]").get()

            }
