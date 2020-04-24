# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from HKJC_database.models import RacingCourse, Jockey_Info, Jockey_Report, Trainer_Info, Trainer_Report, Horse_Info, Horse_Report, Horse_Ranking, Match_Info, Match_Result

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

class HorseInfoItem(DjangoItem):
    django_model = Horse_Info
    pass

class HorseReportItem(DjangoItem):
    django_model = Horse_Report
    pass

class HorseRankingItem(DjangoItem):
    django_model = Horse_Ranking
    pass

class MatchInfoItem(DjangoItem):
    django_model = Match_Info
    pass

class MatchResultItem(DjangoItem):
    django_model = Match_Result
    pass