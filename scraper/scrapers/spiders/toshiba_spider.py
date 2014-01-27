from ..items import Computer
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from scraper.utils import parse_pdf
import tempfile
import urllib2
import os
import json

class ToshibaSpider(CrawlSpider):
    name = "toshiba_spider"
    allowed_domains = ['support.toshiba.com']
    start_urls = [
                    'http://support.toshiba.com/support/home', # this has JS for all computers
    				]
    rules = [ 
    		Rule(SgmlLinkExtractor(allow=['/support/home']), 'parse_urls'),
    		]

    def parse_computer(self, response):
        saveDir = tempfile.mkdtemp()
        sel = Selector(response)

        # make a computer item and populate its fields
        url = response.url
        name = self.getName(sel).encode('utf-8')
        certified = 'Unknown'
        version = 'Unknown'
        parts = self.getParts(saveDir, name)
        source = 'Toshiba'

        name = 'Toshiba ' + name

        # make a computer or update existing
        computer, created = Computer.objects.get_or_create(url=url, name=name, source=source)
        computer.certified = certified
        computer.version = version
        computer.parts = parts # this should be fixed/organized in the Toshiba site
        computer.save()

    ''' Returns name of computer '''
    def getName(self, sel):
        return sel.xpath('//div[@id="breadcrumb-links"]/a[@class="active"]/text()').extract()[0]

    ''' Guess the pdf name and save/convert the first page of the specs manual '''
    def getParts(self, saveDir, name):
        url = 'http://cdgenp01.csd.toshiba.com/content/product/pdf_files/detailed_specs/'
        urlAlt = None

        # sketchy hackery. let's try to guess the url to the pdf.
        if "Satellite Pro" in name:
            url += "satellite_pro_" + name[14:]
        elif "T-Series" in name:
            url += "t-series_" + name[9:].lower()
        elif "All-in-One" in name:
            url += "toshiba_" + name[11:].upper()
        elif "Value-Priced" in name:
            url += "toshiba_" + name[13:]
        elif "TE-Series" in name:
            url += "te_" + name[12:]
        elif "KIRA" in name:
            url += "kirabook" + name[14:].replace(" ", "-")
        elif "mini notebook" in name:
            urlAlt = url + "toshiba_mini_" +name[14:]
            url += "toshiba_mini" + name[14:]
        else:
            urlName = name.replace(" ", "_") # spaces to underscores
            urlName = urlName[0].lower() + urlName[1:] # first letter is lower case
            url += urlName

        pdf = ''
        try:
            pdf = urllib2.urlopen(url + '.pdf')
            print 'success on ' + name
        except:
            try:
                pdf = urllib2.urlopen(url.lower() + '.pdf')
                print 'success lower on ' + name
            except:
                if urlAlt:
                    try:
                        pdf = urllib2.urlopen(urlAlt + '.pdf')
                        print 'success on alt ' + name
                    except:
                        print 'failed on ' + name + ' tried ' + urlAlt
                        pass
                else:
                    print 'failed on ' + name + ' tried ' + url

        parts = ''
        if pdf:
            #print pdf
            os.chdir(saveDir)
            pdfFile = open('file.pdf', 'w')
            pdfFile.write(pdf.read())
            pdfFile.close()
            parts = parse_pdf(saveDir)

        return parts

    ''' Follow urls from JSON in homepage with list of all laptops and desktops '''
    def parse_urls(self, response):
    	sel = Selector(response)
        baseURL = 'http://support.toshiba.com/support/modelHome?freeText='

        # this gets the script tag we want
        script = sel.xpath('//script').extract()[8]

        # super clever extraction of the json
        start = script.find("eval(") + 5
        end = script.find('}]}]}})') + 6
        script = script[start:end]

        # get all the mids
        mids = []
        jsonScript = json.loads(script)
        for family in jsonScript["2756709"]["family"]:
            for model in family["models"]:
                mids.append(model["mid"])
        
        for mid in mids:
            yield Request(baseURL + mid, callback=self.parse_computer)