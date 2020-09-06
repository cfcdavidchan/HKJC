import sys
from datetime import datetime
from pathlib import Path
import twisted
from twisted.internet.task import deferLater
race_number = sys.argv[1]

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
get_project_settings()

def create_directory():
    today = datetime.now().strftime("%d-%m-%Y")
    Path("./RealTime_data/{}".format(today)).mkdir(parents=True, exist_ok=True)

def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(twisted.internet.reactor, seconds, lambda: None)

def crawl_RealTime():
    process = CrawlerProcess(get_project_settings())
    process.crawl('RealTime_crawler', input='inputargument', race_number=race_number)
    process.start()

if __name__ == '__main__':
    create_directory()
    crawl_RealTime()
