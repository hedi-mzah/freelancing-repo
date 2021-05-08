import scrapy


class XxxSpider(scrapy.Spider):
    name = 'xxx'
    allowed_domains = ['xxx.com']
    start_urls = ['https://www.glassdoor.com/Job/us-jobs-SRCH_IL.0,2_IN1.htm?includeNoSalaryJobs=true&p=1']

    def parse(self, response):
        list=response.css('.react-job-listing')
        print(len(list))
        print('####################################################################################')
        for row in list :
            date=row.css('.d-flex.align-items-end.pl-std.css-mi55ob ::text').get()
            position=row.css('.jobLink.css-1rd3saf.eigr9kq2 span::text').get()
            address=response.css('.pr-xxsm.css-1ndif2q.e1rrn5ka0 ::text').get()
            company_name=response.css('.css-l2wjgv.e1n63ojh0.jobLink span ::text').get()
            yield {
                    'date':date,
                    'position':position,
                    'address':address,
                    'company_name':company_name            
            }
