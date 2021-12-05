import scrapy
import re
from geopy.geocoders import Nominatim

class ZooplaSpider(scrapy.Spider):
    name='zoopla'
    start_urls=['https://www.zoopla.co.uk/to-rent/property/edinburgh/?price_frequency=per_month&q=Edinburgh&results_sort=newest_listings&search_source=to-rent#listing_59237736']
    custom_settings={
        'FEED_URI':'data_zoopla_edinburgh.csv',
        'FEED_FORMAT':'csv'
        }
    
    def find_coordinates(self,address):
        geolocator=Nominatim(user_agent='manu')
        location=geolocator.geocode(address)

        if location:
            latitude=location.latitude
            longitude=location.longitude
        else:
            latitude=None
            longitude=None
        
        return latitude,longitude


    def parse_property(self,response):
        
        title=response.xpath('//span[@class="css-1dfc15y-DisplayTitleLabel ep4jli5"]/text()').get()
        address=response.xpath('//span[@class="css-1o06bum-DisplayAddressLabel ep4jli4"]/text()').get()
        price=response.xpath('//span[@class="css-dob1au-PricingLabel ep4jli10"]/text()').get()
        description=response.xpath('//div[@class="css-1sui95d-RichText ep7k4g50"]/span/text()').getall()
        features=response.xpath('//ul[@class="css-1ibzupy-BulletList-FeaturesList ei8ghzj2"]/li/text()').getall()
        number_of_beds= response.xpath('//span[(@data-testid="beds-label") and (@class="css-8rvu8h-AttributeLabel ep4jli0")]/text()').get()
        number_of_baths=response.xpath('//span[(@data-testid="baths-label") and (@class="css-8rvu8h-AttributeLabel ep4jli0")]/text()').get()
        images=response.xpath('//div[@class="css-1i4h94a-SlideImageWrapper e16xseoz0"]/picture/source/@srcset').get()
        images=re.findall('https://lid.zoocdn.com/u/\d+/\d+/\w+\.jpg:p',images)

        letting_agent_name=response.xpath('//p[@class="css-1g2z706-Text-AgentName e1swwt8d3"]/text()').get()
        available_from=response.xpath('//span[@class="css-1f6ruxg-AvailableFrom ep4jli1"]/text()').get()

        #latitude,longitude=self.find_coordinates(address)
        #'latitude':latitude,'longitude':longitude,
        
        yield {'title':title,'address':address,'price':price,'description':description,'features':features,'number_beds':number_of_beds,
        'number_baths':number_of_baths,'images':images,'letting_agent_name':letting_agent_name,'available_from':available_from}
        


    def parse(self,response):
        
        partial_urls=response.xpath('//div[@class="css-mww4lt-StyledContent e2uk8e21"]/a[@class="e2uk8e20 css-1rzeb2c-StyledLink-Link-StyledLink e33dvwd0"]/@href').getall()
        if len(partial_urls)<1:
            print('\n\n URLs with properties are not responding')
        for url in partial_urls:
            url_base='https://www.zoopla.co.uk'
            yield response.follow(url_base+url,callback=self.parse_property)
            
        next_page_button_link=response.xpath('//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]/a[@class="eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse)
        else:
            print('\n\nNext-page _button_link is not responding\n\n')