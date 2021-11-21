import scrapy


class Project1Spider(scrapy.Spider):
    name = 'project1'
    allowed_domains = ['https://www.sellbrite.com/blog/shopify-experts/?utm_source=google&utm_medium=cpc&utm_campaign=11614748316&gclid=Cj0KCQiA4feBBhC9ARIsABp_nbUxm5SNY3OVMLIJzsgaiYX2pVCRR0UwarLmldkQjb5yFvgVRXDRBMcaAmemEALw_wcB']
    start_urls = ['http://www.sellbrite.com/blog/shopify-experts/?utm_source=google&utm_medium=cpc&utm_campaign=11614748316&gclid=Cj0KCQiA4feBBhC9ARIsABp_nbUxm5SNY3OVMLIJzsgaiYX2pVCRR0UwarLmldkQjb5yFvgVRXDRBMcaAmemEALw_wcB/']

    def parse(self, response):
        title = response.css("h1::text").get()        

        heading = response.css(".elementor-widget-container p::text").extract()
        heading = heading[1]

        data = response.css(".elementor-widget-container p::text").extract()
        data = data[10:16]

        # A function that can convert a list to string using comma's 
        def listToString(s):

            # initialize an empty string
            str1 = ""

            # traverse in the string
            for ele in s:
                str1 += ele

            # return string
            return str1
        yield 
        {
                'Title': title,
                'Heading': heading,
                'Data':data
        }
