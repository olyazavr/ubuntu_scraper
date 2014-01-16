from django.db import models
from scrapy.contrib.djangoitem import DjangoItem
from separatedvaluesfield.models import SeparatedValuesField

class Hardware(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=200)
    computersCertifiedIn = SeparatedValuesField(max_length=1000)
    computersEnabledIn = SeparatedValuesField(max_length=1000)
    certified = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class HardwareItem(DjangoItem):
    django_model = Hardware

    ''' Gets the name of the hardware '''
    def getName(self, sel):
        return sel.xpath('//p[@class="large"]/strong/text()').extract()[0]

    ''' Returns a list of certified/enabled computers for the part without garbled html.
        Make sure model is either "certified" or "enabled" depending on which list
        of computers is needed.'''
    def computersIn(self, sel, model):
        computersList = []
        # computers is a list of computers with html
        computers = sel.xpath("//li[@class='model " + model + "']/p").extract()
        for text in computers:
            # format is <p> part1 <a href="..."/> part2 </a> part3 </p>
            part1 = text[text.find('p>') + 2 : text.find('<a')]
            part2 = text[text.find('">') + 2 : text.find('</a')]
            part3 = text[text.find('a>') + 2 : text.find('</p')]
            computersList.append(part1+part2+part3)
        return computersList

    ''' If there is at least one machine with this hardware that is certified, then the 
        machine is certified. Otherwise, we check if it's enabled. If it's none of 
        these, it's unknown.'''
    def getCertification(self, certList, enabList):
        if certList:
            return "Certified"
        if enabList:
            return "Enabled"
        return "Unknown"


class Computer(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=200)
    cid = models.CharField(max_length=200)
    certified = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    parts = SeparatedValuesField(max_length=1000)

    def __unicode__(self):
        return self.name

class ComputerItem(DjangoItem):
    django_model = Computer

    ''' Gets the name of the computer '''
    def getName(self, sel):
        return sel.xpath('//p[@class="large"]/strong/text()').extract()

    ''' Returns the cid of the computer. Not sure if this is a made up value 
        by ubuntu but it makes for a nice id.'''
    def getCid(self, sel):
        # cid is 123456-12345 format
        return sel.xpath('//a[@class="btn"]/@href').re("\d+-\d+")

    ''' Returns whether the computer is Certified or Enabled'''
    def getCertification(self, sel):
        # title() makes the first letter uppercase for maximum prettiness
        return sel.xpath('//div[@class="release"]').extract().title()

    ''' Returns the Ubuntu version that works for this computer.'''
    def getVersion(self, sel):
        # version is 12.12(.12) format
        return sel.xpath('//div[@class="release"]/h3/text()').re("\d+.\d+.?\d*")

    ''' Gets the list of parts in this computer '''
    def getParts(self, sel):
        return sel.xpath('//div[@id="hardware-overview"]/dl/dd/text()').extract()