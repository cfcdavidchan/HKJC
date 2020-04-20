# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from HKJC_database.models import Going, RacingCourse, Jockey

class HkjcCrawlerItem(DjangoItem):
    # define the fields for your item here like:
    going = Jockey
    pass

class JockeyItem(DjangoItem):
    django_model = Jockey