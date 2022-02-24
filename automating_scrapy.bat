@ECHO OFF
ECHO checking if cd is executed
CALL C:\Users\usuario\Platzi\portfolio\Property_let_analysis_with_scrapy_zoopla\venv\Scripts\activate.bat
CALL cd C:\Users\usuario\Platzi\portfolio\Property_let_analysis_with_scrapy_zoopla\zoopla_scraper\zoopla_scraper\spiders
ECHO checking if scrapy is executed
CALL scrapy crawl zoopla -o zoopla_edinburgh.csv

