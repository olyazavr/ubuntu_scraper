from scraper.models import Computer, Hardware
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request

class DellSpider(CrawlSpider):
    name = "dell_spider"
    allowed_domains = ['dell.com']
    start_urls = [
        'http://www.dell.com/support/my-support/us/en/19/Products/laptop', # all laptops
        'http://www.dell.com/support/my-support/us/en/19/Products/desktop', # all desktops
    ]
    rules = [ 
        Rule(SgmlLinkExtractor(allow=['/support/my-support/us/en/19/Products/laptop/\w+']), 'parse_links'), # laptop make
        Rule(SgmlLinkExtractor(allow=['/support/my-support/us/en/19/Products/desktop/\w+']), 'parse_links'), # desktop make
    ]

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        # get the actual url, not the driver url
        url = response.url.replace("drivers", "my-support").replace("product/", "product-support/product/")
        name = self.getName(sel)

        # if there is no information, drop it
        if name == 'drop': 
            return

        certified = 'Unknown'
        version = 'Unknown'
        parts = self.getParts(sel)
        source = 'Dell'

        # if the computer is too old, drop it
        if parts == 'drop':
            return

        # make a computer or update existing
        computer, created = Computer.objects.get_or_create(url=url, name=name, source=source)
        computer.certified = certified
        computer.version = version
        computer.save()
        
        for part in parts:
            if computer not in part.computersIn.all():
                part.computersIn.add(computer)
                part.save()

    def getName(self, sel):
        ''' Returns name of computer '''
        
        # this applies if there are drivers found
        name = sel.xpath('//div[@class="gsd_subSectionHeading"]/text()').extract()
        # if we didn't find anything or we found a weird external thing, drop it
        if not name: 
            return 'drop'

        name = name[0].strip()

        if 'External' in name: 
            return 'drop'

        return 'Dell ' + name
    
    def getParts(self, sel):
        ''' Get audio, video, chipset, and network parts from the drivers list. 
        Return "drop" if the release date is older than 2010. '''

        # we don't care about things older than 2010
        releaseDate = sel.xpath('//div[@class="padding20right ReleaseDate gsd_bodyCopyMedium"]/text()').extract()[0].strip()
        if int(releaseDate[-2:]) < 10: 
            return 'drop'

        # sections are correlated with their DriverItem children (but are not within the same tag), 
        # so obtain the indicies of the sections we care about
        allSections = sel.xpath('//h3[@class="uif_ecTitle gsd_bodyTitleMedium"]/text()').extract()
        wantedSections = []
        for i, section in enumerate(allSections):
            if 'Audio' in section or 'Video' in section or 'Network' in section or 'Chipset' in section:
                wantedSections.append(i)

        partsParsed = []
        partNames = []
        parts = []
        # get the actual drivers that belong to the sections we want
        for i in wantedSections:
            # the div that contains a span with text "(Driver)" THIS IS TOO COOL
            partsParsed.extend(sel.xpath('//div[@class="uif_ecContent gsd_bodyCopyMedium uif_ecCollapsed"][' 
                + str(i+1) + ']//div[contains(span, "(Driver)")]/a[@id="DriverDetailslnk"]/text()').extract())

        # clean up and split the parts
        for part in partsParsed:
            # ignore windows, not sure why this is in here to start with
            if part != 'Windows 7, 8 & 8.1 64bit Operating Systems':
                partNames.extend(self.cleanUp(part))

        for part in partNames:
            hardware, created = Hardware.objects.get_or_create(name=part)
            if created:
                hardware.source = 'Dell'
                hardware.save()
            parts.append(hardware)

        return parts
    
    def parse_links(self, response):
        ''' Find all of the links to computers (they have some weird 
            javascript stuff so we can't just click them) and convert 
            them to the link to the drivers. '''

        sel = Selector(response)
        baseURL = 'http://www.dell.com'

        links = sel.xpath('//div[@id="productFamiliesContainer"]/div/div/a/@href').extract()

        # change the link to the driver link
        for link in links:
            link = link.replace("my-support", "drivers").replace("product-support/", "")
            yield Request(baseURL + link, callback=self.parse_computer)

    def cleanUp(self, part):
        ''' Clean up the name of the part, return a list of 1 or more
            parts (frequently input is a bunch of comma separated parts) '''

        # remove funky unicode or weird stuff
        part = part.replace('Driver', '').replace('Install', '').replace('Application', '')
        part = part.replace('Installation', '').replace('Software', '').replace('driver', '')
        part = part.replace('(R)', '').replace(u'\u2122', '').replace(u'\xae', '')

        # remove driver information
        if ", v" in part:
            part = part[:part.find(", v")]
        elif "for " in part:
            part = part[part.find("for ") + 4:]
        if "(except" in part:
            part = part[:part.find("(except")]
        elif "supporting" in part:
            part = part[:part.find("supporting")]
        elif "(Consumer" in part:
            part = part[:part.find("(Consumer")]

        part = part.strip()

        # for some reason, parts are often multiple comma separated parts
        multParts = part.split(', ')

        # however, sometimes it was actually meant to be a list 
        # ie. Intel Centrino Advanced-N 2230, GT620, GT625
        if len(multParts) > 1:
            if ' ' not in multParts[1]:
                multParts = [part]

        return multParts