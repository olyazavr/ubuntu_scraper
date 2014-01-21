from scrapy.contrib.djangoitem import DjangoItem
from ..models import Hardware, Computer

class HardwareItem(DjangoItem):
    django_model = Hardware

class ComputerItem(DjangoItem):
    django_model = Computer