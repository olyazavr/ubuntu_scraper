from ..items import ComputerItem
from selenium import webdriver
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from scraper.utils import parse_pdf
import re
import time
import tempfile

class ToshibaSpider(CrawlSpider):
    name = "toshiba_spider"
    allowed_domains = ['support.toshiba.com']
    start_urls = [
                    'http://support.toshiba.com/support/home', # this has JS for all computers
    				]
    rules = [ 
    		Rule(SgmlLinkExtractor(allow=['/support/home']), 'parse_urls'),
    		]

    def parse_computer(self, response):
        saveDir = tempfile.mkdtemp()
        sel = Selector(response)

        # make a computer item and populate its fields
        computer = ComputerItem()
        computer['url'] = response.url
        computer['name'] = self.getName(sel)
        computer['certified'] = 'Unknown'
        computer['version'] = 'Unknown'
        computer['parts'] = self.getParts(saveDir, response.url)
        computer['source'] = 'Toshiba'

        # save to Django!
        computer.save()

    ''' Returns name of computer,with Toshiba in front to allow for better searching '''
    def getName(self, sel):
        return 'Toshiba ' + sel.xpath('//div[@id="breadcrumb-links"]/a[@class="active"]/text()').extract()[0]

    ''' Click the link, '''
    def getParts(self, saveDir, url):
        driver = self.setupDriver(saveDir)
        driver.get(url) # go to page with computer model

        # click on manuals tab to see links
        tab = driver.find_element_by_xpath('//div[@id="tabs"]/ul/li[@id="manualsSpecsTab"]')
        tab.click()
        link = None
        parts = ''

        try: # some are ".. .pdf"
            link = driver.find_element_by_partial_link_text(".pdf") 
        except:
            try: # some are "Detailed specs ..."
                link = driver.find_element_by_partial_link_text("Detailed specs") 
            except: # we didn't find anything ):
                pass 
        
        if link != None:
            link.click() # pdf automatically saved once we open this
            time.sleep(2) # make sure we save the file before processing
            parts = parse_pdf(saveDir)

        # now to close everything
        for window in driver.window_handles:
            driver.switch_to_window(window);
            driver.close();

        return parts

    def setupDriver(self, saveDir):
        #this is for downloading pdfs
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", saveDir)
        # this will save every pdf we find
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference('pdfjs.disabled', True) # pdfjs screws up saving pdfs

        driver = webdriver.Firefox(firefox_profile=fp)
        return driver

    ''' Follow urls from JSON in homepage with list of all computers'''
    def parse_urls(self, response):
    	sel = Selector(response)
        baseURL = 'http://support.toshiba.com/support/modelHome?freeText='

        # this gets the script tag we want
        script = sel.xpath('//script').extract()[8]

        # we only care about "mid":"1200007643"
        midsList = re.findall('"mid":"\d+"', script)
        
        for mid in midsList:
            midNum = re.findall("\d+", mid)[0] # parse out the non-numbers 
            yield Request(baseURL + midNum, callback=self.parse_computer)