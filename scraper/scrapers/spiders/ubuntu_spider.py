from ..items import Hardware, Computer
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class UbuntuSpider(CrawlSpider):
    name = "ubuntu_spider"
    allowed_domains = ['ubuntu.com']
    start_urls = [
                    'http://www.ubuntu.com/certification/catalog/makes/', # hardware catalog
                    'http://www.ubuntu.com/certification/desktop/', # computers
    				]
    rules = [ # these are where the spider is allowed to crawl (including diff page #s of these pages)
    		Rule(SgmlLinkExtractor(allow=['/certification/catalog/make/\w+/'])), # list of hardware for a make
    		Rule(SgmlLinkExtractor(allow=['/certification/catalog/component/.+']), 'parse_hardware'), # particular hardware
            Rule(SgmlLinkExtractor(allow=['/certification/desktop/make/\w+/'])), # list of all computers for a make
            Rule(SgmlLinkExtractor(allow=['/certification/hardware/\d+-\d+/']), 'parse_computer') # particular computer
    		]

    def parse_hardware(self, response):
    	sel = Selector(response)

    	# make a hardware item and populate its fields
    	url = response.url
    	name = self.getName(sel)
    	computersCertifiedIn = self.computersIn(sel, "certified")
    	computersEnabledIn = self.computersIn(sel, "enabled")
        source = 'Ubuntu'

        if name != "None None": # because seriously, what the hell is None None
            # make a hardware or update existing
            hardware, created = Hardware.objects.get_or_create(url=url, name=name, source=source)
            hardware.computersCertifiedIn = computersCertifiedIn
            hardware.computersEnabledIn = computersEnabledIn
            hardware.save()

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        url = response.url
        name = self.getName(sel)
        certified = self.getCertification(sel)
        version = self.getVersion(sel)
        parts = self.getParts(sel)
        source = 'Ubuntu'

        # make a computer or update existing
        computer, created = Computer.objects.get_or_create(url=url, name=name, source=source)
        computer.certified = certified
        computer.version = version
        computer.parts = parts # this should be fixed/organized in the Toshiba site
        computer.save()

    ''' Gets the name of the hardware/computer '''
    def getName(self, sel):
        return sel.xpath('//p[@class="large"]/strong/text()').extract()[0]

    ''' Returns a list of certified/enabled computers for the part without garbled html.
        Make sure model is either "certified" or "enabled" depending on which list
        of computers is needed.'''
    def computersIn(self, sel, model):
        computersList = []
        # computers is a list of computers with html
        computers = sel.xpath("//li[@class='model " + model + "']/p").extract()
        for text in computers:
            # format is <p> part1 <a href="..."/> part2 </a> part3 </p>
            part1 = text[text.find('p>') + 2 : text.find('<a')]
            part2 = text[text.find('">') + 2 : text.find('</a')]
            part3 = text[text.find('a>') + 2 : text.find('</p')]
            computersList.append(part1+part2+part3)
        # flatten to comma separated string
        return ', '.join([str(x) for x in computersList])

    ''' Returns whether the computer is Certified or Enabled'''
    def getCertification(self, sel):
        # title() makes the first letter uppercase for maximum prettiness
        return sel.xpath('//div[@class="release"]').re("certified|enabled")[0].title()

    ''' Returns the Ubuntu version that works for this computer.'''
    def getVersion(self, sel):
        # version is 12.12(.12) format
        return sel.xpath('//div[@class="release"]/h3/text()').re("\d+.\d+.?\d*")[0]

    ''' Gets the list of parts in this computer '''
    def getParts(self, sel):
        partsList =  sel.xpath('//div[@id="hardware-overview"]/dl/dd/text()').extract()
        # flatten to comma separated string
        return ', '.join([str(x) for x in partsList])