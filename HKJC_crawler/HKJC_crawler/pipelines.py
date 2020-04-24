# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import JockeyInfoItem, JockeyReportItem, CourseItem, TrainerInfoItem, TrainerReportItem, HorseInfoItem, HorseReportItem, HorseRankingItem, MatchInfoItem, MatchResultItem
from HKJC_database.models import Jockey_Info, RacingCourse, Jockey_Report, Trainer_Info, Trainer_Report, Horse_Info, Horse_Report, Horse_Ranking, Match_Info, Match_Result

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
                item.save()
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


class HorseCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HorseInfoItem):
            trainer = Trainer_Info.objects.get(hkjc_id=item['trainer'])  # get the foregin key from Jockey_info
            item['trainer'] = trainer
            try:  # check whether the horse data exists data exists in Horse_Info
                Horse_Info_data = Horse_Info.objects.get(name=item['name'])
                # if it is exists, update it
                HorseInfo_Item = item.save(commit=False)
                HorseInfo_Item.id = Horse_Info_data.id
                HorseInfo_Item.save()
            except Horse_Info.DoesNotExist: #save it if any amount is changed/ not exists
                print ('Save Data:')
                item.save()

        if isinstance(item, HorseRankingItem):
            horse = Horse_Info.objects.get(hkjc_id=item['horse'])
            item['horse'] = horse
            try: #check whether the horse ranking exists data exists in Horse_Ranking
                ranking_data = Horse_Ranking.objects.get(horse= item['horse'],
                                                      rank= item['rank'],
                                                      rank_reord_date= item['rank_reord_date']
                                                      )
            except Horse_Ranking.DoesNotExist:#save it if the field not exist
                print ('Save Data:')
                item.save()

        if isinstance(item, HorseReportItem):
            horse = Horse_Info.objects.get(hkjc_id=item['horse'])
            item['horse'] = horse
            try: #check whether the horse ranking exists data exists in Horse_Ranking
                HorseReport_data = Horse_Report.objects.get(horse= item['horse'],
                                                            current_rank= item['current_rank'],
                                                            season_start_rank= item['season_start_rank'],
                                                            season_stakes= item['season_stakes'],
                                                            total_stakes= item['total_stakes']
                                                            )
            except Horse_Report.DoesNotExist:#save it if the field not exist
                print ('Save Data:')
                item.save()

        return item

class MatchCrawlerPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, MatchInfoItem):
            try:# check whether the
                match = Match_Info.objects.get(match_date= item['match_date'],
                                               race_number= item['race_number'])
            except Match_Info.DoesNotExist: # save the jockey info if it is not in the db
                item.save()
                pass

        if isinstance(item, MatchResultItem):
            try:  # check whether the
                match_result = Match_Result.objects.get(match= item['match'],
                                                        horse= item['horse'],
                                                        actual_weight= item['actual_weight'],
                                                        declar_weight= item['declar_weight'],
                                                        draw= item['draw'],
                                                        finish_time= item['finish_time'],
                                                        horse_no= item['horse_no'],
                                                        horse_place= item['horse_place'],
                                                        jockey= item['jockey'],
                                                        win_odds= item['win_odds']
                                                        )

            except Match_Result.DoesNotExist: # save it if any amount is changed/ not exists
                item.save()
        return item