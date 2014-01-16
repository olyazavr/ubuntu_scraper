from django.db import models
from dynamic_scraper.models import Scraper, SchedulerRuntime
from scrapy.contrib.djangoitem import DjangoItem
from separatedvaluesfield.models import SeparatedValuesField


class UbuntuCertificationSite(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
    scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name


class Hardware(models.Model):
    name = models.CharField(max_length=200000)
    computersCertifiedIn = SeparatedValuesField(max_length=10000000)
    computersEnabledIn = SeparatedValuesField(max_length=10000000)
    certified = models.CharField(max_length=20000000)
    site = models.ForeignKey(UbuntuCertificationSite)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

class HardwareItem(DjangoItem):
    django_model = Hardware


class Computer(models.Model):
    name = models.CharField(max_length=200)
    parts = SeparatedValuesField(max_length=1000)
    certified = models.CharField(max_length=200)
    cid = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    site = models.ForeignKey(UbuntuCertificationSite)
    url = models.URLField()
    checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.name

class ComputerItem(DjangoItem):
    django_model = Computer
