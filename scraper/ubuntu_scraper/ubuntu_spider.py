from scraper.models import HardwareItem, ComputerItem
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
    	hardware = HardwareItem()
    	hardware['url'] = response.url
    	hardware['name'] = hardware.getName(sel)
    	hardware['computersCertifiedIn'] = hardware.computersIn(sel, "certified")
    	hardware['computersEnabledIn'] = hardware.computersIn(sel, "enabled")

        if hardware['name'] != "None None": # because seriously, what the hell is None None
            # save to Django!
            hardware.save()

    def parse_computer(self, response):
        sel = Selector(response)

        # make a computer item and populate its fields
        computer = ComputerItem()
        computer['url'] = response.url
        computer['name'] = computer.getName(sel)
        computer['cid'] = computer.getCid(sel)
        computer['certified'] = computer.getCertification(sel)
        computer['version'] = computer.getVersion(sel)
        computer['parts'] = computer.getParts(sel)

        # save to Django!
        computer.save()