import scrapy


class Project3Spider(scrapy.Spider):
    name = 'project3'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus//']

    def parse(self, response):
        selector_link = response.xpath("//td/a")
        
        glob_list = []
        country_name = []

        for i in selector_link:
            name = i.xpath(".//text()").get()
            glob_list.append(name)
        
        for elem in glob_list:
            if(type(elem) == str):
                country_name.append(elem)
            else:
                pass

        yield{
                'Name': country_name
            }


