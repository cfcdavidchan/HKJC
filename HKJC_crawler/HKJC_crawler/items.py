# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from HKJC_database.models import RacingCourse, Jockey_Info, Jockey_Report, Trainer_Info, Trainer_Report

class HkjcCrawlerItem(DjangoItem):
    # define the fields for your item here like:
    pass

class JockeyInfoItem(DjangoItem):
    django_model = Jockey_Info
    pass

class JockeyReportItem(DjangoItem):
    django_model = Jockey_Report
    pass

class CourseItem(DjangoItem):
    django_model = RacingCourse
    pass

class TrainerInfoItem(DjangoItem):
    django_model = Trainer_Info
    pass

class TrainerReportItem(DjangoItem):
    django_model = Trainer_Report
    pass