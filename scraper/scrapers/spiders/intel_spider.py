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
        for i in xrange(processors):
            # make a processor item and populate its fields
            url = self.getUrl(sel, xpath, i)
            name = self.getName(sel, xpath, i, processors)

            # the processors on this page are old, we don't want them
            if name == 'drop':
                return

            graphics = self.getGraphics(sel, xpath, i)

            # make a processor or update existing
            processor, created = Processor.objects.get_or_create(url=url, name=name, source=source)
            processor.codename = codename
            processor.graphics = graphics
            processor.save()

    def getUrl(self, sel, xpath, i):
        ''' Returns url of processor '''

        return 'http://ark.intel.com' + sel.xpath(xpath + '/td[2]/a/@href').extract()[i]

    def getName(self, sel, xpath, i, numProcessors):
        ''' Returns name of processor '''

        names = sel.xpath(xpath + '/td[2]/a/text()').extract()

        # name is split into "name" and "GHz", so we want every other one
        if len(names) != 2 * numProcessors:
            # if this isn't the case, the processor is prehistoric, drop it
           return 'drop'

        # replace the strange unicode things to facilitate seraching
        return names[2 * i].strip().replace(u'\xae', '').replace(u'\N{TRADE MARK SIGN}', '')

    def getCodename(self, sel):
        ''' Finds the codename of the current page of processors '''

        # format: "Products (formerly codename)"
        name = sel.xpath('//div[@class="l"]/h1/text()').extract()[0]
        return name[name.find("Formerly") + 9 : -1]

    def getGraphics(self, sel, xpath, i):
        ''' Get the graphics associated with the processor '''

        graphics = sel.xpath(xpath + '/td[8]/text()').extract()
        if graphics:
            return graphics[i].strip().replace(u'\xae', '').replace(u'\N{TRADE MARK SIGN}', '')
        return ''

    def parse(self, response):
        ''' This is the first thing called upon visiting ark.intel.com 
            Visits every processor page. '''

        sel = Selector(response)
        baseURL = 'http://ark.intel.com'
        urls = sel.xpath('//div[@id="ProductsByCodeName-ProcessorCodeNames-scrollpane"]//a/@href').extract()

        for url in urls:
            yield Request(baseURL + url, callback=self.parse_processors)