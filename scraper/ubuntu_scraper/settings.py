import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hardware.settings") 

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.ubuntu_scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')
NEWSPIDER_MODULE = 'scraper.ubuntu_scraper'

ITEM_PIPELINES = [
    #'scraper.ubuntu_scraper.pipelines.UbuntuScraperPipeline',
]
