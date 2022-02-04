# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import string
from itemadapter import ItemAdapter
import sqlite3


class ZooplaScraperPipeline:
    def __init__(self):
        self.con=sqlite3.connect('zoopla.db')
        self.cur=self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS edinburgh(title TEXT,address TEXT,price REAL,letting_agent_name TEXT)""")
        #self.cur.execute("""CREATE TABLE IF NOT EXISTS edinburgh(address TEXT, letting_agent_name TEXT, number_of_baths REAL, number_of_beds REAL, price REAL,title TEXT,images TEXT, available_from TEXT, property_url TEXT,description TEXT,features TEXT)""")
                                                               
        


    def process_item(self, item, spider):
        self.cur.execute("""INSERT OR IGNORE INTO edinburgh VALUES(?,?,?,?)""",(item['title'],item['address'],item['price'],item['letting_agent_name']))
        #self.cur.execute("INSERT OR IGNORE INTO edinburgh VALUES(?,?,?,?,?,?,?,?,?,?,?)",(item['address'],item['letting_agent_name'],item['number_of_baths'],item['number_of_beds'],item['price'],item['title'],item['images'],item['available_from'],item['property_url'],item['description'],item['features']))
        self.con.commit()
        return item
        
        