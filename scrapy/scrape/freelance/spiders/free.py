
#you should pip install those lib  before running the  script
#then run "scrapy crawl free -o test1.csv "from your terminal
import scrapy
import json
from scrapy.crawler import CrawlerProcess

class FreeSpider(scrapy.Spider):
    name = 'free'
    start_urls = ['https://takafulalarabia.com/MedicalNetwork/p/']


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

        for page in range(219):


            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& '+str(page+1)+' &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            url=self.start_urls[0]+str(page+1)+'.html'
            print(url)
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        list=response.css('.item ::attr(href)').getall()
        print('********************************************')
        print(len(list))
        for link in list :
            print('######################################################################### #################################################################')
            print(link)
            yield scrapy.Request(url = link , callback = self.parseprofile)


    def parseprofile(self, response):
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ profile ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        category='مركز'
        categories = ['مختبر' , 'عيادة' , 'صيدلي'   , 'مجمع'  ,'مستشفى'  , 'نظارات'  ,   'مركز','بصريات'   ]
        phone=[i.attrib['href'] for i in response.css('.numb a') ]
        title=response.css('.title::text').get()
        for i in categories:
            if i in title:
                category = i
        address=response.css('.location::text').get()
        googlemap_address_url=response.css('.GoogleMaps a::attr(href)').get()
        region=response.css('.list-unstyled li:nth-child(2) a::text').get()
        city=response.css('.list-unstyled li:nth-child(3) a::text').get()
        discount_details={}
        for row in response.css('.itemPrice'):
            discount_details[row.css('::text').get().strip(' \n\t*.,')]=row.css('span::text').get()
            discount_details[row.css('span::text').get()]=row.css('::text').get().strip(' \n\t*.')
        dic= {
                'title' :title ,
                'phone':phone ,
                'address' :address ,
                'googlemap_address_url' :googlemap_address_url ,
                'region' :region ,
                'city' :city ,
                'discount_details': discount_details ,
                'category' : category,
                'url' : response.url,
        }
        print(dic)
        yield dic



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
