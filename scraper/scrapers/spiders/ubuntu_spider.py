from scraper.models import Hardware, Computer
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import re

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

        if name == "None None": # because seriously, what the hell is None None
            return; 

    	computersIn = self.computersIn(sel)
        source = 'Ubuntu'

        # make a hardware or update existing
        hardware, created = Hardware.objects.get_or_create(name=name, source=source)
        hardware.url = url
        hardware.computersIn = computersIn
        hardware.save()

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        url = response.url
        name = self.getName(sel)

        # if it's a computer pretending to be hardware, discard it
        if name == 'drop':
            return

        certified = self.getCertification(sel)
        version = self.getVersion(sel)
        parts = self.getParts(sel)
        source = 'Ubuntu'

        # make a computer or update existing
        computer, created = Computer.objects.get_or_create(url=url, source=source)
        if created: # only update name if we're creating
            computer.name = name
        computer.certified = certified
        computer.version = version
        computer.save()

        for part in parts:
            if computer not in part.computersIn.all():
                part.computersIn.add(computer)
                part.save()

    def getName(self, sel):
        ''' Gets the name of the hardware/computer '''

        name = sel.xpath('//p[@class="large"]/strong/text()').extract()[0]
        category = sel.xpath('//p[@class="large"]/strong/text()').extract()[1]

        # if it's a "system" it's just a computer trying to be a hardware piece.
        # drop that shit.
        if category == 'System':
            return 'drop'

        return self.cleanUp(name)

    def computersIn(self, sel):
        ''' Returns a list of computers for the part.'''

        computerInfo = []
        computersList = []
        baseURL = 'http://www.ubuntu.com/'
        # computers is a list of computers with html
        computers = sel.xpath("//ul[@class='models']/li/p").extract()
        certifications = sel.xpath("//ul[@class='models']/li/@class").extract()
        for i, text in enumerate(computers):
            # format is <p> part1 <a href="..."/> part2 </a> part3 </p>
            part1 = text[text.find('p>') + 2 : text.find('<a')]
            part2 = text[text.find('">') + 2 : text.find('</a')]
            part3 = text[text.find('a>') + 2 : text.find('</p')]
            url =  baseURL + text[text.find('f="') + 3 : text.find('/">')]
            certification = certifications[i][6:].title()

            # we don't care about servers
            if 'server' not in part3 and 'Server' not in part3:
                computerInfo.append(((part1+part2+part3), url, certification))
        
        for (name, url, certification) in computerInfo:
            computer, created = Computer.objects.get_or_create(url=url, source='Ubuntu')
            if created:
                computer.name = name
                computer.certified = certification
                computer.version = 'Unknown'
                computer.save()
            computersList.append(computer)
        return computersList
    
    def getCertification(self, sel):
        ''' Returns whether the computer is Certified or Enabled'''

        # title() makes the first letter uppercase for maximum prettiness
        return sel.xpath('//div[@class="release"]').re("certified|enabled")[0].title()
    
    def getVersion(self, sel):
        ''' Returns the Ubuntu version that works for this computer.'''

        # version is 12.12(.12) format
        return sel.xpath('//div[@class="release"]/h3/text()').re("\d+.\d+.?\d*")[0]

    def getParts(self, sel):
        ''' Gets the list of parts in this computer. We only care about processors,
            video, and network '''

        # find which parts we care about
        allSections = sel.xpath('//div[@id="hardware-overview"]/dl/dt/text()').extract()
        wantedSections = []
        for i, section in enumerate(allSections):
            if 'Processor' in section or 'Video' in section or 'Network' in section:
                wantedSections.append(i)

        # only get the parts we care about
        parts = []
        for i in wantedSections:
            part = sel.xpath('//div[@id="hardware-overview"]/dl/dd/text()').extract()[i]

            # make it look nice
            part = self.cleanUp(part)

            if 'Not Specified' not in part and 'Unknown' not in part: 
                hardware, created = Hardware.objects.get_or_create(name=part, source='Ubuntu')
                if created:
                    hardware.save()
                parts.append(hardware)

        return parts

    def cleanUp(self, part):
        ''' Clean up the name of the part '''

        # remove funky unicode or weird stuff
        part = part.replace('Intel(R) ', '').replace('[', '').replace(']', '')
        part = part.replace(' processor Graphics Controller', '').replace('(TM)', '')
        part = part.replace('AMD AMD', 'AMD').replace('(R)', '').replace('(tm)', '')
        part = part.replace('\x2f', '/').replace('\x20', ' ')

        # try to make the processor name similar to Intel's
        if 'CPU' in part:
            part = part.replace(' CPU', '')
            part = part[: part.find('@')] + 'Processor'
            # Intel Core i3 530 Processor should be i3-530
            if re.match('Intel Core i\d \d{3} Processor', part):
                part = part[:part.find('i') + 1] + '-' + part[part.find('i') + 3 :]
            # Intel Core i3 M 330 Processor should be i3-330M
            elif re.match('Intel Core i\d M \d{3} Processor', part):
                part = part[:part.find('i') + 1] + '-' + part[part.find('M') + 2 : part.find('M') + 5] + 'M' + part[part.find('M') + 5 :]


        # remove multiple whitespaces
        part = ' '.join(part.split())

        return part
