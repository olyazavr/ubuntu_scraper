from scrapy.exceptions import DropItem

# not using this atm primarily because I have no idea how to
class UbuntuScraperPipeline(object):
    def process_item(self, item, spider):
        return item