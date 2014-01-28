from ..items import Computer
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
        # computer, created = Computer.objects.get_or_create(url=url, name=name, source=source)
        # computer.certified = certified
        # computer.version = version
        # computer.parts = parts # this should be fixed/organized in the Toshiba site
        # computer.save()
        

    def getName(self, sel):
        ''' Returns name of computer '''
        
        # this applies if there are drivers found
        name = sel.xpath('//div[@class="gsd_subSectionHeading"]/text()').extract()
        if not name: # otherwise, nothing was found, throw it out
            return 'drop'
        return 'Dell ' + name[0].encode('utf-8').strip()
    
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

        parts = []
        # get the actual drivers that belong to the sections we want
        for i in wantedSections:
            parts += sel.xpath('//div[@class="uif_ecContent gsd_bodyCopyMedium uif_ecCollapsed"][' +
                    str(i+1) + ']//div[contains(span, "(Driver)")]/a[@id="DriverDetailslnk"]/text()').extract()

        # clean up the name
        for i, part in enumerate(parts):
            if ", v" in part:
                parts[i] = part[:part.find(", v")]
            elif "for " in part:
                parts[i] = part[part.find("for ") + 4:]
            elif " driver" in part.lower():
                parts[i] = part[:part.lower().find(" Driver")]
            elif " Install" in part:
                parts[i] = part[:part.find(" Install")]
            elif " Software" in part:
                parts[i] = part[:part.find(" Software")]
            elif " Application" in part:
                parts[i] = part[:part.find(" Application")]

        return parts
    
    def parse_links(self, response):
        ''' Find all of the links to computers (they have some weird javascript stuff so we 
        can't just click them) and convert them to the link to the drivers. '''

        sel = Selector(response)
        baseURL = 'http://www.dell.com/'

        links = sel.xpath('//div[@id="productFamiliesContainer"]/div/div/a/@href').extract()

        # change the link to the driver link
        for link in links:
            link = link.replace("my-support", "drivers").replace("product-support/", "")
            yield Request(baseURL + link, callback=self.parse_computer)