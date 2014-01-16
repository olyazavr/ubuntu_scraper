from dynamic_scraper.spiders.django_spider import DjangoSpider
from scraper.models import UbuntuCertificationSite, Hardware, HardwareItem


class HardwareSpider(DjangoSpider):

    name = 'hardware_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(UbuntuCertificationSite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Hardware
        self.scraped_obj_item_class = HardwareItem
        super(HardwareSpider, self).__init__(self, *args, **kwargs)