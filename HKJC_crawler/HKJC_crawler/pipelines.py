# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import JockeyInfoItem, JockeyReportItem, CourseItem, TrainerInfoItem, TrainerReportItem
from HKJC_database.models import Jockey_Info, RacingCourse, Jockey_Report, Trainer_Info, Trainer_Report

class JockeysCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JockeyInfoItem):
            jockeyInfo_item = item.save(commit=False)
            try:# check whether the jockey exists in jockey_info
                Jockey_data = Jockey_Info.objects.get(name= item['name'])
                # if it is exists, update it
                jockeyInfo_item.id = Jockey_data.id
                jockeyInfo_item.save()
            except Jockey_Info.DoesNotExist: # save the jockey info if it is not in the db
                jockeyInfo_item.save()

        if isinstance(item, JockeyReportItem):
            Jockey = Jockey_Info.objects.get(name=item['jockey']) #get the foregin key from Jockey_info
            item['jockey'] = Jockey
            JockeyReport_item = item.save(commit=False)
            try:  # check whether the Jockey Report data exists in Jockey_Report
                Jockey_Report_data = Jockey_Report.objects.get(jockey=item['jockey'],
                                                               stakes_won= item['stakes_won'],
                                                               wins_past_10_racing= item['wins_past_10_racing'],
                                                               avg_JKC_past_10= item['avg_JKC_past_10'],
                                                               number_win= item['number_win'],
                                                               number_second= item['number_second'],
                                                               number_third= item['number_third'],
                                                               number_fourth= item['number_fourth'],
                                                               total_rides= item['total_rides'],
                                                               win_rate= item['win_rate'],
                                                               )
            except Jockey_Report.DoesNotExist: # save it if any amount is changed/ not exists
                print ('Save Data:')
                JockeyReport_item.save()
        return item

class CoursesCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CourseItem):

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

class TrainersCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, TrainerInfoItem):
            TrainerInfo_item = item.save(commit=False)
            try:# check whether the trainer exists in jockey_info
                Trainer_data = Trainer_Info.objects.get(name= item['name'])
                # if it is exists, update it
                TrainerInfo_item.id = Trainer_data.id
                print ('save_data')
                TrainerInfo_item.save()
            except Trainer_Info.DoesNotExist: # save the jockey info if it is not in the db
                print ('save_data')
                TrainerInfo_item.save()

        if isinstance(item, TrainerReportItem):
            Trainer = Trainer_Info.objects.get(name=item['trainer']) #get the foregin key from Jockey_info
            item['trainer'] = Trainer
            TrainerReport_item = item.save(commit=False)
            try:  # check whether the Jockey Report data exists in Jockey_Report
                Trainer_Report_data = Trainer_Report.objects.get(trainer=item['trainer'],
                                                                 stakes_won= item['stakes_won'],
                                                                 wins_past_10_racing= item['wins_past_10_racing'],
                                                                 number_win= item['number_win'],
                                                                 number_second= item['number_second'],
                                                                 number_third= item['number_third'],
                                                                 number_fourth= item['number_fourth'],
                                                                 total_runners= item['total_runners'],
                                                                 win_rate= item['win_rate']
                                                                 )
            except Trainer_Report.DoesNotExist: # save it if any amount is changed/ not exists
                print ('Save Data:')
                TrainerReport_item.save()
        return item