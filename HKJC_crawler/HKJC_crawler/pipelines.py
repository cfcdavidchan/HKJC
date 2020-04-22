# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import JockeyItem, CourseItem
from HKJC_database.models import Jockey, RacingCourse

class JockeysCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JockeyItem):
            #jockey_item = item.save(commit=False)
            Jockey_exist = Jockey.objects.filter(name= item['name'],
                                                 chinese_name= item['chinese_name'],
                                                 hkjc_id= item['hkjc_id'],
                                                 stakes_won= item['stakes_won'],
                                                 wins_past_10_racing= item['wins_past_10_racing'],
                                                 avg_JKC_past_10= item['avg_JKC_past_10'],
                                                 number_win= item['number_win'],
                                                 number_second= item['number_second'],
                                                 number_third= item['number_third'],
                                                 number_fourth= item['number_fourth'],
                                                 total_rides= item['total_rides'],
                                                 win_rate= item['win_rate']
                                                 )

            if not Jockey_exist: # save the jockey if it is not in the db
                item.save()
                pass
            else: # not save if it is exists
                pass

        return item

class CourseCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CourseItem):
            # jockey_item = item.save(commit=False)
            Course_exist = RacingCourse.objects.filter(place=item['place'],
                                                       chinese_place=item['chinese_place'],
                                                       course=item['course'],
                                                       home_straight_M=item['home_straight_M'],
                                                       width_M= item['width_M'],
                                                       )
            if not Course_exist:  # save the jockey if it is not in the db
                #item.save()
                pass
            else: # not save if it is exists
                pass

        return item
