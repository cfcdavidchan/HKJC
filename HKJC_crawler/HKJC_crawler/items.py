# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HkjcCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    horse_name = scrapy.Field()
    weight = scrapy.Field()
    jockey = scrapy.Field()
    trainer = scrapy.Field()
    crawl_time = scrapy.Field()
    pass
