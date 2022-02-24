# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import Identity, TakeFirst, MapCompose,Join
import datetime

import re
import pandas as pd

def convert_to_number(word):
    number=re.sub('[£a-zA-Z, ]','',word)
    number=int(number)
    return number
    
def convert_to_datetime(word): 
     
    if 'immediately' in word:
        date=datetime.date.today()
    else:
        date=re.findall('\d\d? \w+ \d\d\d\d',word)
        date=datetime.datetime.strptime(date[0], '%d %B %Y')
        
    return date



class ZooplaScraperItem(scrapy.Item):

    title=scrapy.Field(input_processor=MapCompose(),output_processor=TakeFirst())
    address=scrapy.Field(output_processor=TakeFirst())
    price=scrapy.Field(input_processor=MapCompose(convert_to_number),output_processor=TakeFirst())
    description=scrapy.Field(input_processor=Join(),output_processor=TakeFirst())
    features=scrapy.Field(input_processor=Join(),output_processor=TakeFirst())
    number_of_beds=scrapy.Field(input_processor=MapCompose(convert_to_number),output_processor=TakeFirst())
    number_of_baths=scrapy.Field(input_processor=MapCompose(convert_to_number),output_processor=TakeFirst())
    images=scrapy.Field(input_processor=Join(),output_processor=TakeFirst())
    letting_agent_name=scrapy.Field(output_processor=TakeFirst())
    available_from=scrapy.Field(input_processor=MapCompose(convert_to_datetime),output_processor=TakeFirst())
    property_url=scrapy.Field(output_processor=TakeFirst())
    incorporation_date=scrapy.Field(output_processor=TakeFirst())
    #agency=scrapy.Field(input_processor=TakeFirst())
    #latitude=scrapy.Field()
    #longitude=scrapy.Field()
