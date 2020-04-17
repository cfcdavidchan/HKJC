from HKJC_crawler.items import HkjcCrawlerItem
import scrapy
import re
from datetime import datetime

class OddSpider(scrapy.Spider):
    name = 'Odd_crawler'
    allowed_domains = ['bet.hkjc.com']
    start_urls = ['https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=en']

    def parse(self, response):
        url = self.start_urls[0]
        yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        item = HkjcCrawlerItem()

        all_horse = response.xpath('//script[contains(., "var infoDivideByRaceEn")]').re('infoDivideByRaceEn(.*);;')[0].split('|')[1:]
        all_jcokey = response.xpath('//script[contains(., "var jockeysByRace")]').re('jockeysByRace(.*);;')[0].split('|')[1:]
        all_trainer = response.xpath('//script[contains(., "var trainersByRace")]').re('trainersByRace(.*);;')[0].split('|')[1:]
        all_weight = response.xpath('//script[contains(., "var drawWgtByRace")]').re('drawWgtByRace(.*)')[0].split(';;')[2]
        all_weight = re.findall('[|][0-9][0-9][0-9]', all_weight)
        all_weight = [weight.replace('|','') for weight in all_weight]
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M")

        try:
            for horse, jockey, trainer, weight in zip(all_horse, all_jcokey, all_trainer, all_weight):
                item['horse_name'] = horse
                item['weight'] = weight
                item['jockey'] = jockey
                item['trainer'] = trainer
                item['crawl_time'] = current_time
                yield item
        except:
            pass


