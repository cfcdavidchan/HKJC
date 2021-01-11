import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import js2xml
from js2xml.utils.vars import get_vars
from .helper.helper import get_horse_chi_name, get_jockey_chi_name, get_trainer_chi_name, get_horse_game_history, get_result_by_distance, get_class_change, get_hourse_condition, get_horse_age, get_recent_time_record

from pprint import pprint
import csv
import requests
import sys

class RecentMatchSpider(scrapy.Spider):
    name = 'RecentMatch_crawler_v2'
    allowed_domains = ['bet.hkjc.com']
    start_urls = ['https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=ch']
    match_content = dict()

    def parse(self, response):
        url = self.start_urls[0]
        # get match data
        match_info = response.xpath('//div[@class="mtgInfoDV"]//text()').extract()
        # get match date
        self.match_date = match_info[0]
        self.match_date = self.match_date[:self.match_date.find(',')]
        self.match_date = datetime.strptime(self.match_date, '%d/%m/%Y')
        self.match_date = datetime.strftime(self.match_date, '%Y/%m/%d')
        self.match_content['match_date'] = self.match_date
        # get the chinese match venue
        self.match_place = [match_info[-1]]
        # get the english match venue
        englist_info = requests.get('https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=en')
        englist_info = BeautifulSoup(englist_info.content, 'html.parser') #Get the English place name
        match_place_eng = englist_info.find('div', attrs={'class': "mtgInfoDV"}).text
        match_place_eng = match_place_eng.split(',')[-1]
        match_place_eng = match_place_eng.lower().strip()
        self.match_place.append(match_place_eng)
        self.match_content['match_place'] = self.match_place
        # count number of match
        number_of_match = len(response.xpath('//div[contains(@id, "raceSel")]').extract())
        for race_number in range(1, number_of_match + 1):
            match_info_url = 'https://bet.hkjc.com/racing/index.aspx/?lang=en&date={}&raceno={}'.format(self.match_date, race_number)
            yield scrapy.Request(match_info_url, callback=self.match_detail, meta={'race_number': race_number})

    def match_detail(self, response):
        # get race number
        race_number = response.meta.get('race_number')
        race_number_str = 'Race {}'.format(race_number)
        self.match_content[race_number_str] = dict()
        # get race Info
        race_info = response.xpath('//div[contains(@style, "float:left;vertical-align:middle;width:85%")]/span[contains(@class, "content")]//text()').extract()
        race_time = race_info[3].replace(',','').lower().strip()
        race_class = race_info[5].replace(',','').lower().strip()
        race_course = race_info[7].replace(',','').lower().strip()
        # position will be different depending on the track
        if race_course == 'ALL WEATHER TRACK'.lower().strip():
            race_track = 'all weather track'
            race_distance = race_info[9].replace(',', '').lower().replace('m', '').strip()
        else:
            race_track = race_info[9].replace(',', '').upper().strip().replace('COURSE', '').replace('"', '')
            race_distance = race_info[11].replace(',','').lower().replace('m','').strip()
        self.match_content[race_number_str]['Race Info'] = [race_time, race_class, race_course, race_track, race_distance]
        self.match_content[race_number_str]['Race Horse'] = dict()
        # Create dict for all horse in this race
        race_horse_dict = dict()
        # Create all 14 horse space
        for horse_num in range(1,15):
            race_horse_dict[horse_num] = dict()
            race_horse_dict[horse_num]['draw'] = int()
            # priority to run
            race_horse_dict[horse_num]['star'] = False
            # trump card
            race_horse_dict[horse_num]['plus'] = False
            # chi name
            race_horse_dict[horse_num]['name'] = ""
            race_horse_dict[horse_num]['age'] = int()
            # chi jockey name
            race_horse_dict[horse_num]['jockey'] = ""
            # chi trainer name
            race_horse_dict[horse_num]['trainer'] = ""
            race_horse_dict[horse_num]['last 6 Runs'] = list()
            race_horse_dict[horse_num]['same distance game result'] = list()
            race_horse_dict[horse_num]['class change'] = ""
            race_horse_dict[horse_num]['game_history_class'] = list()
            race_horse_dict[horse_num]['last game date'] = ""
            race_horse_dict[horse_num]['last game date delta'] =""
            race_horse_dict[horse_num]['status'] = ""
            race_horse_dict[horse_num]['average_record_time'] = 0.0

            # crawl all horse data
        all_horse = response.xpath('//div[contains(@class,"bodyMainOddsTable content")]/script[contains(@type,"text/javascript")]').extract_first()
        all_horse = all_horse[len('<script type="text/javascript">    \r\n    '):all_horse.rfind(';')+len(";")]
        all_horse = get_vars(js2xml.parse(all_horse))
        all_horse = all_horse['normalRunnerList'][race_number]
        for horse in all_horse:
            horse_number = horse['num']
            # check horse number in race_horse_dict
            if horse_number not in race_horse_dict.keys():
                continue
            # draw
            try:
                horse_draw = horse["barDraw"]
                race_horse_dict[horse_number]['draw'] = horse_draw
            except KeyError:
                pass
            # star
            try:
                star = True if horse["priority"] == "Y" else False if horse["priority"] == "N" else None
                race_horse_dict[horse_number]['star'] = star
            except KeyError:
                pass
            # plus
            try:
                plus = True if horse["trumpCard"] == "Y" else False if horse["trumpCard"] == "N" else None
                race_horse_dict[horse_number]['plus'] = plus
            except KeyError:
                pass
            # name
            try:
                horse_chi_name = horse["nameCh"]
                race_horse_dict[horse_number]['name'] = horse_chi_name
            except KeyError:
                pass
            # age
            try:
                horse_eng_name = horse["nameEn"]
                horse_horse_age = get_horse_age(horse_eng_name)
                race_horse_dict[horse_number]['age'] = horse_horse_age
            except KeyError:
                pass
            # jockey
            try:
                jockey_chi_name = horse["jockeyNameCh"]
                race_horse_dict[horse_number]['jockey'] = jockey_chi_name
            except KeyError:
                pass
            # trainer
            try:
                trainer_chi_name = horse["trainerNameCh"]
                race_horse_dict[horse_number]['trainer'] = trainer_chi_name
            except KeyError:
                pass
            # last 6 Runs
            try:
                horse_eng_name = horse["nameEn"]
                horse_game_history = get_horse_game_history(horse_eng_name)
            except:
                horse_game_history = None
            try:
                all_place = []
                for game in horse_game_history:  # loop all the match
                    try:
                        place = int(game[1])
                    except ValueError:
                        place = 7  # name as 7 if no place
                    all_place.append(place)

                while len(all_place) < 6:  # if not enough 6 past game
                    all_place.append(7)  # name as 7 for that match

                race_horse_dict[horse_number]['last 6 Runs'] = all_place[:6]
            except:
                race_horse_dict[horse_number]['last 6 Runs'] = []
            # same distance game result
            try:
                same_distance = get_result_by_distance(list_game_game_history=horse_game_history,
                                                       race_distance= int(race_distance),
                                                       match_place=self.match_place[-1],
                                                       race_course=race_course)
                race_horse_dict[horse_number]['same distance game result'] = same_distance
            except:
                pass
            # class change, game_history_class
            try:
                game_history_class, class_change = get_class_change(game_history=horse_game_history,
                                                                    current_class=race_class)
                race_horse_dict[horse_number]['class change'] = class_change
                race_horse_dict[horse_number]['game_history_class'] = game_history_class
            except:
                pass
            # last game date
            try:
                last_game_date, last_game_days_delta, status = get_hourse_condition(game_history=horse_game_history,
                                                                                    match_date_str=self.match_date)
                race_horse_dict[horse_number]['last game date'] = last_game_date
                race_horse_dict[horse_number]['last game date delta'] = last_game_days_delta
                race_horse_dict[horse_number]['status'] = status
            except:
                pass

            try:
                average_recent_time = get_recent_time_record(horse_name=horse_eng_name, reference_year= 3, match_place=self.match_place[-1], distance=int(race_distance))
                race_horse_dict[horse_number]['average_record_time'] = average_recent_time
            except:
                print ("average_recent_time error")
                pass


        self.match_content[race_number_str]['Race Horse'] = race_horse_dict

    def closed(self, reason):
        pprint(self.match_content)
        total_race = len(self.match_content.keys()) - 2
        print (total_race)
        print('Spider ended:', reason)
        with open('recent_match.csv', 'w') as recent_csv:
            wr = csv.writer(recent_csv, quoting=csv.QUOTE_ALL)
            heeder_row = ['' for i in range(11)]
            heeder_row += ['Match Date:', self.match_content['match_date'],'','Match Place:', self.match_content['match_place']]
            for race_num in range(1, total_race + 1):
                race_key = 'Race {}'.format(race_num)
                # race_row = ['' for i in range(11)] + [race_key]

                match_date = self.match_content['match_date']
                match_course = ''
                if self.match_content[race_key]['Race Info'][2] == 'ALL WEATHER TRACK'.lower():
                    match_course = '田泥'
                else:
                    if self.match_content['match_place'][-1] == 'sha tin':
                        match_course = '田草'
                    if self.match_content['match_place'][-1] == 'happy valley':
                        match_course = '谷草'
                match_class = self.match_content[race_key]['Race Info'][1]
                match_distance = self.match_content[race_key]['Race Info'][4]
                track = self.match_content[race_key]['Race Info'][3]
                # match_info = ['' for i in range(11)] + ['Match Time:', match_date,
                #                                         '',
                #                                         '班次:', match_class,
                #                                         '',
                #                                         '跑道:', self.match_content[race_key]['Race Info'][2],
                #                                         '',
                #                                         '賽道:', track,
                #                                         '',
                #                                         '賽程:', match_distance,
                #                                         ]
                wr.writerow (['日期', '場次', '跑道', '班次', '路程', '賽道', '場地狀況', '預計步速', '預計疊數', '預計跑法', '評分優勢',
                              '馬號', '王牌', '優先', '檔位', '馬名', '馬齡', '騎師', '練馬師',
                              'last game 1', 'last game 2', 'last game 3', 'last game 4', 'last game 5', 'last game 6',
                              '同路程次數', '同路程冠', '同路程亞', '同路程季', '同路程殿',
                              '上場班次','兩場前班次','三場次班次','升/降班', '上次比賽日', '離上次比賽日數', '狀態', '平均圈速'
                              ])
                for horse_num, horse_detail in self.match_content[race_key]['Race Horse'].items():
                    horse_row = [match_date, race_key, match_course, match_class, match_distance, track]
                    for i in range(5):
                        horse_row.append('')
                    horse_row.extend([horse_num, horse_detail['plus'], horse_detail['star'], horse_detail['draw'], horse_detail['name'], horse_detail['age'], horse_detail['jockey'], horse_detail['trainer']])
                    for place in horse_detail['last 6 Runs']:
                        horse_row.append(place)
                    for result in horse_detail['same distance game result']:
                        horse_row.append(result)
                    for i in range(3):
                        try:
                            content = horse_detail['game_history_class'][i]
                            horse_row.append(content)
                        except:
                            horse_row.append('No game history')
                    horse_row.append(horse_detail['class change'])
                    horse_row.append(horse_detail['last game date'])
                    horse_row.append(horse_detail['last game date delta'])
                    horse_row.append(horse_detail['status'])
                    horse_row.append(horse_detail['average_record_time'])
                    wr.writerow(horse_row)


