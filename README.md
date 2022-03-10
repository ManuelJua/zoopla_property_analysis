# zoopla_property_analysis
This is a web scraper made with Scrapy. I have been running this scraper on zoopla.co.uk for about a month before being blocked by robots.txt. Nevertheless I could gather some data about properties to rent in Edinburgh, Scotland, UK. Most of the info is in the spider folder. Its path is zoopla_property_analysis/spiders/. There you will find the following files:

zoopla_spider.py -- Spider

zoopla_edinburgh.csv --- All the collected info is here

data_zoopla_analysis.ipynb --- Jupyter notebook with a brief analysis of the information in zoopla_edinburgh.csv

zoopla_cleaning.py -- Just a script to remove duplicates from the csv file, as the spraper didn't do that by itself. I made an attempt to put everthing in a sqlite3 database through a pipeline but didn't work

In addition, in zoopla_property_analysis/ folder there is a bat file created in order to run the scraper automatically through the task scheduler in Windows
