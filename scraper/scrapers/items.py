from scrapy.contrib.djangoitem import DjangoItem
from scraper.models import Hardware, Computer, Processor

class HardwareItem(DjangoItem):
    django_model = Hardware

class ComputerItem(DjangoItem):
    django_model = Computer

class ProcessorItem(DjangoItem):
    django_model = Processor