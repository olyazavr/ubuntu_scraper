from scraper.models import Computer, Processor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
import re

class ToshibaSpider(CrawlSpider):
    name = "toshiba_spider"
    allowed_domains = ['toshiba.com']
    totalItems = '1000' # for pagination; there are really only about 100, but just to be safe
    start_urls = [
            'http://www.toshiba.com/us/laptop-finder?target=laptops.to&rpp=' + totalItems, # all laptops
            'http://www.toshiba.com/us/desktop-finder?target=desktops.to&rpp=' + totalItems, # all desktops
    ]
    rules = [
        Rule(SgmlLinkExtractor(allow=['/us/computers/laptops/\w+/.*'], 
                            deny='/us/computers/laptops/.*/reviews'), 'get_specs'), # particular laptop
        Rule(SgmlLinkExtractor(allow=['/us/computers/desktops/\w+/.*'],
                            deny='/us/computers/desktops/.*/reviews'), 'get_specs'), # particular desktop
    ]

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        url = response.url
        name = self.getName(sel)
        certified = 'Unknown'
        version = 'Unknown'
        parts = self.getParts(sel)
        source = 'Toshiba'

        # make a computer or update existing
        computer, created = Computer.objects.get_or_create(url=url, source=source)
        computer.name=name
        computer.certified = certified
        computer.version = version
        computer.parts = parts
        computer.save()

    def getName(self, sel):
        ''' Returns name of computer '''

        name = sel.xpath('//div[@id="Hero-Intro"]/h1/text()').extract()[0]
        # remove funky unicode to facilitate searching
        name = name.replace(u'\N{TRADE MARK SIGN}', '').replace(u'\xe9', '').replace(u'\xae', '')
        return 'Toshiba ' + name

    def getParts(self, sel):
        ''' Get all the possible parts we care about (video, audio, 
            network, graphics) '''

        processors = self.getPart(sel, "Performance", "ProcessorCentralProcessingUnit")
        graphics = self.getPart(sel, "Performance", "GraphicsGraphicsProcessingUnit")
        wireless = self.getPart(sel, "Communication", "Wireless")

        # get rid of GHz in processors
        for i in xrange(len(processors)):
            if ', (' in processors[i]:
                processors[i] = processors[i][:processors[i].find(", (")] 
            elif ' (' in processors[i]:
                processors[i] = processors[i][:processors[i].find(" (")] 
            elif 'processor' in processors[i]: # this makes me angry
                processors[i] = processors[i].replace('processor', 'Processor')

        # intel HD graphics is not useful, find the graphics via processors
        if 'Mobile Intel HD Graphics' in graphics:
            for proc in processors:
                try:
                    graphics.append(Processor.objects.filter(name=proc)[0].graphics)
                    graphics.remove('Mobile Intel HD Graphics')
                except:
                    pass # ):

        return processors + graphics + wireless

    def getPart(self, sel, divisionName, javascriptTag):
        ''' Gets all the parts from the specified division, that start with the
            particular javascript tag '''

        allDivision = sel.xpath('//div[contains(h4, "' + divisionName + '")]/dl').extract()[0]
        # we want between the divistion and the next division
        allDivision = '<' + allDivision[allDivision.find("('" + javascriptTag + "')"):]
        # removes the next divison
        allDivision = re.split('</dd>\s*<dt', allDivision)[0]

        parts = re.split('<[ a-zA-Z0-9"=/\()\']*>', allDivision)

        # clean up
        unwanted = ['*', 'Choose from:', u'\xab', 'current selection']
        parts = filter(lambda x: x.strip() and x not in unwanted, parts)
        # remove weird unicode to faciliate searching
        parts = map(lambda x: x.strip().replace(u'\xae', '').replace(u'\x99', '')
                                    .replace(u'\u2122', ''), parts)

        return parts

    def get_specs(self, response):
        ''' Goes to the specs page of every computer page '''

        specs = '/specs?pop=true'
        yield Request(response.url + specs, callback=self.parse_computer)