from scraper.models import HardwareItem, ComputerItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

class UbuntuSpider(CrawlSpider):
    name = "ubuntu_spider"
    allowed_domains = ['ubuntu.com']
    start_urls = [
                    'http://www.ubuntu.com/certification/desktop/', # hardware catalog
    				'http://www.ubuntu.com/certification/catalog/makes/' # computers
    				]
    rules = [
    		Rule(SgmlLinkExtractor(allow=['/certification/catalog/make/\w+/'])), # list of hardware for a make
    		Rule(SgmlLinkExtractor(allow=['/certification/catalog/component/.+']), 'parse_hardware'), # particular hardware
            Rule(SgmlLinkExtractor(allow=['/certification/desktop/make/\w+/'])), # list of all computers for a make
            Rule(SgmlLinkExtractor(allow=['/certification/hardware/\d+-\d+']), 'parse_computer') # particular computer
    		]

    def parse_hardware(self, response):
    	sel = Selector(response)

    	# make a hardware item and populate its fields
    	hardware = HardwareItem()
    	hardware['url'] = response.url
    	hardware['name'] = hardware.getName(sel)
    	hardware['computersCertifiedIn'] = hardware.computersIn(sel, "certified")
    	hardware['computersEnabledIn'] = hardware.computersIn(sel, "enabled")
    	hardware['certified'] = hardware.getCertification(hardware['computersCertifiedIn'], hardware['computersEnabledIn'])

    	print hardware['url']
    	print hardware['name']
    	print hardware['computersCertifiedIn']
    	print hardware['computersEnabledIn']
    	print hardware['certified']
    	print '\n'

	def parse_computer(self, response):
		sel = Selector(response)

		# make a computer item and populate its fields
		computer = ComputerItem()
		computer['url'] = response.url
		computer['name'] = computer.getName(sel)
		computer['cid'] = computer.getCid(sel)
		computer['certified'] = computer.getCertification(sel)
		computer['version'] = computer.version(sel)
		computer['parts'] = computer.getParts(sel)

		print computer['url']
		print computer['name']
		print computer['certified']
		print computer['version']
		print computer['parts']
		print '\n'