from ..items import Computer
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
import re

class ToshibaSpider(CrawlSpider):
    name = "toshiba_spider"
    allowed_domains = ['toshiba.com']
    start_urls = [
            'http://www.toshiba.com/us/laptop-finder', # all laptops
            'http://www.toshiba.com/us/desktop-finder', # all desktops
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=['/us/computers/laptops/\w+/.*'], 
                            deny='/us/computers/laptops/.*/reviews'), 'get_specs'), # particular laptop
        Rule(SgmlLinkExtractor(allow=['/us/computers/desktops/\w+/.*'],
                            deny='/us/computers/desktops/.*/reviews'), 'get_specs'), # particular desktop
        Rule(SgmlLinkExtractor(allow=['/us/laptop-finder#.*'])), # next page
        Rule(SgmlLinkExtractor(allow=['//us/desktop-finder#.*'])), # next page
    ]

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        url = response.url
        name = self.getName(sel).encode('utf-8')
        certified = 'Unknown'
        version = 'Unknown'
        parts = self.getParts(sel)
        source = 'Toshiba'

        print url
        print name
        print parts

        # make a computer or update existing
        # computer, created = Computer.objects.get_or_create(url=url, name=name, source=source)
        # computer.certified = certified
        # computer.version = version
        # computer.parts = parts # this should be fixed/organized in the Toshiba site
        # computer.save()
        pass

    def getName(self, sel):
        ''' Returns name of computer '''

        return 'Toshiba ' + sel.xpath('//div[@id="Hero-Intro"]/h1/text()').extract()[0]

    def getParts(self, sel):
        ''' Get all the possible parts we care about (video, audio, 
            network, chipset/graphics) '''

        parts = []

        # chipset
        allPerformance = sel.xpath('//div[contains(h4, "Performance")]/dl').extract()[0]
        # somewhat isolate what we want
        allPerformance = '<' + allPerformance[allPerformance.find("GraphicsGraphicsProcessingUnit"): ]
        parts.append(re.split('<[ a-zA-Z0-9"=/\()\']+>', allPerformance))

        return parts

    def get_specs(self, response):
        specs = '/specs?pop=true'
        print response.url
        yield Request(response.url + specs, callback=self.parse_computer)