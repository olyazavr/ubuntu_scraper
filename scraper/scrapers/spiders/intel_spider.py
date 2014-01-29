from scraper.models import Processor
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http.request import Request

class IntelSpider(BaseSpider): 
    name = "intel_spider"
    allowed_domains = ['ark.intel.com']
    # BaseSpider (not CrawlSpider) means it will call parse() upon going to start_urls
    start_urls = ['http://ark.intel.com/']

    def parse_processors(self, response):
        sel = Selector(response)

        # processors are in a table, with each tr being a particular processor
        xpath = '//div[@id="tabs-All"]/table/tbody/tr'
        codename = self.getCodename(sel)
        source = 'Intel'

        processors = len(sel.xpath(xpath))
        for i in range(processors):
            # make a processor item and populate its fields
            url = self.getUrl(sel, xpath, i)
            name = self.getName(sel, xpath, i)
            graphics = self.getGraphics(sel, xpath, i)

            # make a processor or update existing
            processor, created = Processor.objects.get_or_create(url=url, name=name, source=source)
            processor.codename = codename
            processor.graphics = graphics
            processor.save()

    def getUrl(self, sel, xpath, i):
        ''' Returns url of processor '''

        return 'http://ark.intel.com' + sel.xpath(xpath + '/td[2]/a/@href').extract()[i]

    def getName(self, sel, xpath, i):
        ''' Returns name of processor '''

        name = sel.xpath(xpath + '/td[2]/a/text()').extract()[i]
        # exclude "(20M Cache, 1.90 GHz)"
        return name[:name.find("(")]

    def getCodename(self, sel):
        ''' Finds the codename of the current page of processors '''

        # format: "Products (formerly codename)"
        name = sel.xpath('//div[@class="l"]/h1/text()').extract()[0]
        return name[name.find("Formerly") + 9 : -1]

    def getGraphics(self, sel, xpath, i):
        ''' Get the graphics associated with the processor '''

        graphics = sel.xpath(xpath + '/td[8]/text()').extract()
        if graphics:
            return graphics[i].strip()
        return ''

    def parse(self, response):
        ''' This is the first thing called upon visiting ark.intel.com 
            Visits every processor page. '''

        sel = Selector(response)
        baseURL = 'http://ark.intel.com'
        urls = sel.xpath('//div[@id="ProductsByCodeName-ProcessorCodeNames-scrollpane"]//a/@href').extract()

        for url in urls:
            yield Request(baseURL + url, callback=self.parse_processors)