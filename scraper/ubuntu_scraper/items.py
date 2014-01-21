from scrapy.contrib.djangoitem import DjangoItem
from ..models import Hardware, Computer

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
        # flatten to comma separated string
        return ', '.join([str(x) for x in computersList])

class ComputerItem(DjangoItem):
    django_model = Computer

    ''' Gets the name of the computer '''
    def getName(self, sel):
        return sel.xpath('//p[@class="large"]/strong/text()').extract()[0]

    ''' Returns whether the computer is Certified or Enabled'''
    def getCertification(self, sel):
        # title() makes the first letter uppercase for maximum prettiness
        return sel.xpath('//div[@class="release"]').re("certified|enabled")[0].title()

    ''' Returns the Ubuntu version that works for this computer.'''
    def getVersion(self, sel):
        # version is 12.12(.12) format
        return sel.xpath('//div[@class="release"]/h3/text()').re("\d+.\d+.?\d*")[0]

    ''' Gets the list of parts in this computer '''
    def getParts(self, sel):
        partsList =  sel.xpath('//div[@id="hardware-overview"]/dl/dd/text()').extract()
        # flatten to comma separated string
        return ', '.join([str(x) for x in partsList])