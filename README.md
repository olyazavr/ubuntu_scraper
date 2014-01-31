#Ubuntu Scraper

Scrapes computer and  hardware information into a database using Django and Scrapy.
Retrieves computers and their parts' relationship, and in the case of Ubuntu, checks the certification information (whether or not it can run on Ubuntu and what version).
Certified means Ubuntu will definitely run. Enabled signifies Ubuntu will run only if preinstalled by the manufacturer.

##Setup:
1. install pip
2. install Django with pip
3. install scrapy with pip
4. install south with pip
5. install Postgresql

##To run a spider: 
```$ scrapy crawl <spider_name>```

##Spiders:
1. intel_spider (must be run before toshiba_spider)
2. toshiba_spider
3. dell_spider
4. ubuntu_spider

##To modify the database:
1. modify scraper/models.py
2. If a new model is added, add it to scraper/scrapers/items.py
3. ```$ python manage.py syncdb```
4. ```$ python manage.py schemamigration scraper --auto```
5. ```$ python manage.py migrate scraper```

##To drop/create database:
1. ```$ psql -U scraper scraper ```
2. ```# drop schema public cascase; create schema public;```
3. syncdb/schemamigration/migrate as above
