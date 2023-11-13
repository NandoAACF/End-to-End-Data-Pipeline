import scrapy

class CenterWorldUniversity(scrapy.Spider):
    name = "Center for World University Rankings"
    start_urls = ["http://cwur.org/2023.php"]

    def parse(self, response):

        for university in response.css('tbody > tr'):
            institution = university.css('td:nth-child(2)::text').extract()
            alumni_employment = university.css('td:nth-child(6)::text').extract()

            yield {
                'University': institution,
                'Alumni Employability Rank': alumni_employment,
            }

