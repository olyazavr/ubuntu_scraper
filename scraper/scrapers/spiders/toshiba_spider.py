from ..items import ComputerItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from urlparse import urljoin
import re

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
        sel = Selector(response)

        # # make a computer item and populate its fields
        computer = ComputerItem()
        computer['url'] = response.url
        # computer['name'] = computer.getName(sel)
        # computer['certified'] = computer.getCertification(sel)
        # computer['version'] = computer.getVersion(sel)
        # computer['parts'] = computer.getParts(sel)

        # # save to Django!
        # computer.save()

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
            yield Request(urljoin(baseURL, midNum), callback=self.parse_computer)