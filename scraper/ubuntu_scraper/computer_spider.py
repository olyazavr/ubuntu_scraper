from dynamic_scraper.spiders.django_spider import DjangoSpider
from scraper.models import UbuntuCertificationSite, Computer, ComputerItem


class ComputerSpider(DjangoSpider):

    name = 'computer_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(UbuntuCertificationSite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Computer
        self.scraped_obj_item_class = ComputerItem
        super(ComputerSpider, self).__init__(self, *args, **kwargs)