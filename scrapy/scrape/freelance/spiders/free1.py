
#you should pip install those lib  before running the  script
#then run "scrapy crawl free -o test1.csv "from your terminal
import scrapy
import json
from scrapy.crawler import CrawlerProcess



class FreeSpider(scrapy.Spider):
    name = 'free1'
    start_urls = ['https://directory.sba.gov.sa/firm?page=']


    #header will help to avoid  cruching cause of \bot detection
    headers={

                    'access-control-allow-credentials': 'true',
                    'access-control-allow-origin': 'https://www.youtube.com',
                    'alt-svc': 'h3-Q050="googleads.g.doubleclick.net:443"; ma=2592000,h3-Q050=":443"; ma=2592000,h3-29="googleads.g.doubleclick.net:443"; ma=2592000,h3-29=":443"; ma=2592000,h3-27="googleads.g.doubleclick.net:443"; ma=2592000,h3-27=":443"; ma=2592000,h3-T051="googleads.g.doubleclick.net:443"; ma=2592000,h3-T051=":443"; ma=2592000,h3-T050="googleads.g.doubleclick.net:443"; ma=2592000,h3-T050=":443"; ma=2592000,h3-Q046="googleads.g.doubleclick.net:443"; ma=2592000,h3-Q046=":443"; ma=2592000,h3-Q043="googleads.g.doubleclick.net:443"; ma=2592000,h3-Q043=":443"; ma=2592000,quic="googleads.g.doubleclick.net:443"; ma=2592000; v="46,43",quic=":443"; ma=2592000; v="46,43"',
                    'cache-control': 'no-cache, no-store, must-revalidate',
                    'content-length': '0',
                    'content-type': 'text/html; charset=UTF-8',
                    'expires': 'Fri, 01 Jan 1990 00:00:00 GMT',
                    'location': 'https://googleads.g.doubleclick.net/pagead/id?slf_rd=1',
                    'p3p': 'policyref="https://googleads.g.doubleclick.net/pagead/gcn_p3p_.xml", CP="CURa ADMa DEVa TAIo PSAo PSDo OUR IND UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"',
                    'pragma': 'no-cache',
                    'server': 'cafe',
                    'set-cookie': 'test_cookie=CheckForPermission; expires=Sat, 26-Sep-2020 23:21:34 GMT; path=/; domain=.doubleclick.net; Secure; SameSite=none',
                    'status': '302',
                    'timing-allow-origin': '*',
                    'x-content-type-options': 'nosniff',


    }





    def start_requests(self):
        #this will show  the nbr of page where it stopped  so u can run it again from that page
        #so you just haveto change the range by an intervale like this [111..1774]

        for page in range(97):


            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& '+str(page+1)+' &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            url=self.start_urls[0]+str(page+1)
            print(url)
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        list=response.css('.col-lg-6.col-md-12 a::attr(href)').getall()
        print('********************************************')
        print(len(list))
        for link in list :
            print('######################################################################### #################################################################')
            print(link)
            yield scrapy.Request(url = link , callback = self.parseprofile )


    def parseprofile(self, response):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ profile ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        dict={}
        dict['title'] = response.css('.navy-text.pt-5::text').get().strip(' \n\t')
        dict['office_owner'] = response.css('.navy-text.pt-5 ::text').get().strip(' \n\t')
        for row in response.css('.list-inline-item.px-5 ') :
            try:
                dict[row.css('i').xpath("@class").extract()[0]] =row.css('a::text').get().strip(' \n\t')
            except:
                pass

        # phone = response.css('.fa.fa-phone-square a::text').get()
        # email = response.css('.fa.fa-envelope a::text').get()
        # fax = response.css('.fa.fa-fax a ::text').get()
        # website = response.css('.fa.fa-laptop a::text').get()

        dict['commitment_officer_name'] = response.css('p:nth-child(2) ::text').getall()[1]
        dict['commitment_officer_phone'] = response.css('p:nth-child(6)::text').get()
        dict['commitment_officer_email'] = response.css('p:nth-child(4) ::text').get()
        dict['url']= response.url
        i=-1
        for key in response.css(' .card-body li span strong::text').getall():
            i+=1
            try:
                dict[key]=response.css('.card-body li span::text').getall()[i]
            except :
                pass
        #  الخدمات
        list = response.css('.my-1 a::text').getall()
        dict[' الخدمات'] = [i.strip(' \n\t') for i in list]
        dict['twitter'] =response.css('.scroll-container a::attr(href)').get()
        print(dict)
        yield dict



#this will slow the scraping if your  running on more than 100 page uncomment those
# custom_settings = {
#         #'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
#         #'DOWNLOAD_DELAY': 1
#     }







#
#
#
#     def parsereview(self,response):
#         print("/////////////////////////////////////////////////////////// review //////////////////////////////////////////////////////////////////////////////////")
#         #parse  the review
#         #done
#         name=response.css('#DivisionsDropdownComponent::text').get()
#         rate=response.css('.v2__EIReviewsRatingsStylesV2__large::text').get()
#         CEO_name=response.css('.donut-text.d-lg-table-cell.pt-sm.pt-lg-0.pl-lg-sm div::text').get()
#         CEO_rate=response.css('.numCEORatings::text').get()
#         Recommend_Friend= response.css('.donut__DonutStyle__donutchart_text_val::text').getall()[0]
#         Approve_of_CEO= response.css('.donut__DonutStyle__donutchart_text_val::text').getall()[1]
#
#         y= response.css('.pros .my-0')
#         pros=''
#         for x in y :
#             pros=pros+x.css('a::text').get() + x.css('span::text').get()+x.css('.numReviews::text').get()
#            # pros.append(x.css('.numReviews::text'))
#         y=response.css('.mt-md-md .my-0')
#         cons=''
#         for x in y :
#             cons=cons+x.css('a::text').get() + x.css('span::text').get()+x.css('.numReviews::text').get()
#             #cons.append(x.css('.numReviews::text'))
#
#
#         # pros=x[0].css('a::text').get() + x[0].css('span::text').get()
#         # pros_reviews=x[1].css('span::text').get()
#         dic=response.meta['dic']
#         dic['company_name']=name
#         dic['rate']=rate
#         dic['CEO_name']=CEO_name
#         dic['CEO_rate']=CEO_rate
#         dic['Recommend_Friend']=Recommend_Friend
#         dic['Approve_of_CEO']=Approve_of_CEO
#         dic['pros']=pros
#         dic['cons']=cons
#         yield dic
#         #todo
#         #  pros=response.css('.common__EIReviewHighlightsStyles__highlightText my-0')
#         # cons=response.css('#empReview_36378270 .v2__EIReviewDetailsV2__fullWidth+ .v2__EIReviewDetailsV2__fullWidth span')
#
#
#
#
#
#
#     def parseoverview(self, response):
#         # dic1={}
#         # #review scrapand parse
#         url= 'https://www.glassdoor.co.in'+response.css('.eiCell.cell.reviews::attr(href)').get()
#         # print(url)
#         review_request=scrapy.Request(url=url,callback=self.parsereview)
#
#         print("###################################################################### overview ########################################################################")
#         #parse  the overview
#
#
#
#
#
#         dic=response.meta['dic']
#         dic['activityLevel']=response.css('.activityLevel::text').get()
#         box=response.css('.infoEntity')
#
#         for line in box:
#             if (line.css('label::text').get()=='Website'):
#                 dic[line.css('label::text').get()] = line.css('a::attr(href)').get()
#             else:
#                 dic[line.css('label::text').get()] = line.css('span::text').get()
#
#
#
#
#
#         review_request.meta['dic'] = dic
#         yield review_request
#
#         # website=box[0].css('span::text').get()
#         # Headquarters=box[1].css('span::text').get()
#         # Size=box[2].css('span::text').get()
#         # Founded=box[1].css('span::text').get()
#         # Type=box[1].css('span::text').get()
#         # Industry=box[1].css('span::text').get()
#         # Revenue=box[1].css('span::text').get()
#
#
# #run this  if you run it out scrapy project
# #just uncomment those and run the comment python and the name of the file
#
#
# # if __name__ == '__main__':
# #     process = CrawlerProcess()
# #     process.crawl(ZillowScraper)
# #     process.start()
