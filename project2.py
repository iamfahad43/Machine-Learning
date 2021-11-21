import scrapy


class Project2Spider(scrapy.Spider):
    name = 'project2'
    allowed_domains = ['www.realpython.github.io']
    start_urls = ['http://realpython.github.io/fake-jobs//']

    def parse(self, response):
        title = response.css("h1::text").get()
        head2 = response.css("h2::text").extract()
        head3 = response.css("h3::text").extract()

        JobTitle = [i +" -> "+ j for i, j in zip(head2, head3)]

        LocData = response.css(".content .location::text").extract()

        PostTime = response.css("time[datatime]::text").extract()

        Location = []
        for i in LocData:
            j = i.replace(' ', '')
            Location.append(j)

        yield
        {
                print("The title of page is: \n", title, "\nand jobs posted are: \n", JobTitle, "\Post Time is: \n", PostTime)
        }
