# from scrapy import cmdline
#
#
# cmdline.execute("scrapy crawl Course_crawler".split())

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
get_project_settings()

def crawl_Course():
    process = CrawlerProcess(get_project_settings())
    process.crawl('Course_crawler')
    process.start()

def crawl_Horse():
    process = CrawlerProcess(get_project_settings())
    process.crawl('Horse_crawler')
    process.start()

def crawl_Trainer():
    process = CrawlerProcess(get_project_settings())
    process.crawl('Trainer_crawler')
    process.start()

def crawl_Jockeys():
    process = CrawlerProcess(get_project_settings())
    process.crawl('Jockeys_crawler')
    process.start()

def crawl_Match():
    process = CrawlerProcess(get_project_settings())
    process.crawl('Match_crawler')
    process.start()

def crawl_RecentMatch():
    process = CrawlerProcess(get_project_settings())
    process.crawl('RecentMatch_crawler')
    process.start()


