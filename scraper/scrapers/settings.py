import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hardware.settings") 

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.scrapers.spiders',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')
NEWSPIDER_MODULE = 'scraper.scrapers.spiders'

ITEM_PIPELINES = {
    #'scraper.ubuntu_scraper.pipelines.UbuntuScraperPipeline' : 300,
}
