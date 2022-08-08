import scrapy

BASE_URL = 'https://ng.indeed.com' #'https://de.indeed.com'


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    # start_urls = ['https://de.indeed.com/jobs?q=Data%20Engineer&l&from=searchOnHP&vjk=c16e53614bca7aaa']
    start_urls = ['https://ng.indeed.com/jobs?q=data%20engineer&l&from=searchOnHP&vjk=51eea39502ee4781']

    def parse(self, response, **kwargs):
        for results in response.css('div.result'):
            yield {
                'title': results.css('a.jcs-JobTitle span::text').get(),
                'company': results.css('span.companyName *::text').get(),
                'location': results.css('div.companyLocation::text').get(),
                'link': BASE_URL + results.css('a.jcs-JobTitle').attrib['href'],
            }

        next_to_crawl = set(response.css('ul.pagination-list li a::attr("href")').extract())

        for next_link in next_to_crawl:
            next_page = BASE_URL + next_link

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

# response.css('#searchCountPages::text').get().strip()[10:]