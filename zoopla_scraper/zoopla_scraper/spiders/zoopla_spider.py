import scrapy
from zoopla_scraper.items import ZooplaScraperItem
from scrapy.loader import ItemLoader
#import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

class ZooplaSpider(scrapy.Spider):
    name='zoopla'
    start_urls=['https://www.zoopla.co.uk/to-rent/property/edinburgh/?price_frequency=per_month&q=Edinburgh&results_sort=newest_listings&search_source=to-rent#listing_59237736']
    
    
    def find_coordinates(self,address):
        geolocator=Nominatim(user_agent='manu')
        geocode=RateLimiter(geolocator.geocode,min_delay_seconds=1)
        if address:
            location=geocode(address)

        if location:
            latitude=location.latitude
            longitude=location.longitude
        else:
            latitude=None
            longitude=None
        
        return latitude,longitude


    def parse_property(self,response,**kwargs):

        
        l=ItemLoader(item=ZooplaScraperItem(),selector=response)
    
        l.add_xpath('title','//span[@class="css-jv46e5-DisplayTitleLabel eiwe0nt5"]/text()')
        l.add_xpath('address','//span[@class="css-192hawr-DisplayAddressLabel eiwe0nt4"]/text()')
        l.add_xpath('price','//span[@class="css-dob1au-PricingLabel eiwe0nt13"]/text()')
        l.add_xpath('description','//div[@class="css-1sui95d-RichText ep7k4g50"]/span/text()')
        l.add_xpath('features','//ul[@class="css-1ibzupy-BulletList-FeaturesList edyyq052"]/li/text()')
        l.add_xpath('number_of_beds','//span[(@data-testid="beds-label") and (@class="css-8rvu8h-AttributeLabel eiwe0nt0")]/text()')
        l.add_xpath('number_of_baths','//span[(@data-testid="baths-label") and (@class="css-8rvu8h-AttributeLabel eiwe0nt0")]/text()')
        l.add_xpath('images','//div[@class="css-1i4h94a-SlideImageWrapper e16xseoz0"]/picture/source/@srcset')
        l.add_value('property_url',kwargs['property_url'])
        l.add_xpath('letting_agent_name','//p[@class="css-1g2z706-Text-AgentName e1swwt8d3"]/text()')
        l.add_xpath('available_from','//span[@class="css-1f6ruxg-AvailableFrom eiwe0nt1"]/text()')
        #l.add_xpath('agency','//div[@class="css-o16bi5-AgentNameBlock e1swwt8d4"]/p[@class="css-1g2z706-Text-AgentName e1swwt8d3"]/text()')

        #item['latitude'],item['longitude']=self.find_coordinates(item['address'])
       
        
        yield l.load_item()
        


    def parse(self,response):
        
        partial_urls=response.xpath('//div[@class="css-mww4lt-StyledContent e2uk8e21"]/a[@class="e2uk8e20 css-1rzeb2c-StyledLink-Link-StyledLink e33dvwd0"]/@href').getall()
        if len(partial_urls)<1:
            print('\n\n URLs with properties are not responding')
        for url in partial_urls:
            url_base='https://www.zoopla.co.uk'
            yield response.follow(url_base+url,callback=self.parse_property,cb_kwargs=dict(property_url=url_base+url))
            
        next_page_button_link=response.xpath('//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]/a[@class="eaoxhri5 css-xtzp5a-ButtonLink-Button-StyledPaginationLink eaqu47p1"]/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link,callback=self.parse)
        else:
            print('\n\nNext-page _button_link is not responding\n\n')