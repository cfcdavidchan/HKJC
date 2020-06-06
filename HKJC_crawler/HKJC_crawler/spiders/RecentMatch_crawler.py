import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import pprint
import csv
import requests
import sys

from .helper.helper import get_horse_chi_name, get_jockey_chi_name, get_trainer_chi_name, get_horse_game_history, get_result_by_distance, get_class_change, get_hourse_condition, get_horse_age

class RecentMatchSpider(scrapy.Spider):
    name = 'RecentMatch_crawler'
    allowed_domains = ['bet.hkjc.com']
    start_urls = ['https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=ch']
    match_content = dict()

    def parse(self, response):
        url = self.start_urls[0]
        match_info = response.xpath('//div[@class="mtgInfoDV"]//text()').extract()
        self.match_date = match_info[0]
        self.match_date = self.match_date[:self.match_date.find(',')]
        self.match_date = datetime.strptime(self.match_date, '%d/%m/%Y')
        self.match_date = datetime.strftime(self.match_date, '%Y/%m/%d')
        self.match_content['match_date'] = self.match_date
        self.match_place = [match_info[-1]]  # chinese place name
        # Get the English place name
        englist_info = requests.get('https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=en')
        englist_info = BeautifulSoup(englist_info.content, 'html.parser') #Get the English place name
        match_place_eng = englist_info.find('div', attrs={'class': "mtgInfoDV"}).text
        match_place_eng = match_place_eng.split(',')[-1]
        match_place_eng = match_place_eng.lower().strip()
        self.match_place.append(match_place_eng)

        self.match_content['match_date'] = self.match_date
        self.match_content['match_place'] = self.match_place

        number_of_match = len(response.xpath('//div[contains(@id, "raceSel")]').extract())
        for race_number in range(1, number_of_match+1):
            match_info_url = 'https://bet.hkjc.com/racing/index.aspx/?lang=en&date={}&venue=ST&raceno={}'.format(self.match_date, race_number)
            yield scrapy.Request(match_info_url, callback=self.match_detail)
        #pprint.pprint(self.match_content)

        # match_info_url = 'https://bet.hkjc.com/racing/index.aspx/?lang=en&date={}&venue=ST&raceno={}'.format(self.match_date, 1)
        # yield scrapy.Request(match_info_url, callback=self.match_detail)

    def match_detail(self, response):
        '''
        :param response:
        :return:
                match_content = {'race_number':
                                     {'Race Info': [race_time, race_class, race_course, race_distance],
                                      {'Race Horse': {'number': str(),
                                                      'name': str(),
                                                      'draw': int(),
                                                      'jockey': str(),
                                                      'trainer': str(),
                                                      'last 6 Runs': list(),
                                                      'same distance game result': list(),
                                                      'class change': str()}}},
                                 'match_date': str(),
                                 'match_place': str()

                                 }
        '''

        race_number = response.xpath('//div[contains(@style, "float:left;vertical-align:middle;width:85%")]/span/strong/text()').extract_first()
        self.match_content[race_number] = dict()
        #Race Info
        race_info = response.xpath('//div[contains(@style, "float:left;vertical-align:middle;width:85%")]/span[contains(@class, "content")]//text()').extract()
        race_time = race_info[3].replace(',','').lower().strip()
        race_class = race_info[5].replace(',','').lower().strip()
        race_course = race_info[7].replace(',','').lower().strip()
        race_track = race_info[9].replace(',','').upper().strip().replace('COURSE','').replace('"','')

        if race_course == 'ALL WEATHER TRACK'.lower().strip():
            race_distance = race_info[9].replace(',', '').lower().replace('m', '').strip()
        else:
            race_distance = race_info[11].replace(',','').lower().replace('m','').strip()
        self.match_content[race_number]['Race Info'] = [race_time, race_class, race_course, race_track, race_distance]
        self.match_content[race_number]['Race Horse'] = dict()
        print ('\n\n')
        print (race_number)
        print(self.match_content[race_number]['Race Info'])
        #Race Horse
        all_horse = response.xpath('//tr[contains(@height, "22px")]').extract()
        #loop over horse
        for horse in all_horse:
            horse = BeautifulSoup(horse, "html.parser")
            horse = horse.select("td[class*='tableContent']")

            # Draw if no draw then skip it
            skip_row = False
            horse_draw = horse[5].get_text().strip()

            try:
                horse_draw = int(horse_draw)
                #self.match_content[race_number]['Race Horse']['draw'] = horse_draw
            except ValueError:
                skip_row = True

            if skip_row:
                continue
            # Horse number
            Horse_number = horse[1].get_text()
            try:
                Horse_number = int(Horse_number)
            except:
                Horse_number = 0
            self.match_content[race_number]['Race Horse'][Horse_number] = dict()
            self.match_content[race_number]['Race Horse'][Horse_number]['draw'] = horse_draw

            #star or plus
            star = False
            plus = False
             #get all horse image
            imgs = horse[0].findAll('img')
            for img in imgs:
                src = img['src']
                if 'star' in src:
                    star = True
                if 'plus' in src:
                    plus = True

            self.match_content[race_number]['Race Horse'][Horse_number]['star'] = star
            self.match_content[race_number]['Race Horse'][Horse_number]['plus'] = plus

            # Horse Name, Horse Chi Name
            horse_name = horse[3].get_text().strip()
            horse_chi_name = get_horse_chi_name(horse_name)
            horse_horse_age = get_horse_age(horse_name)
            self.match_content[race_number]['Race Horse'][Horse_number]['name'] = horse_chi_name
            self.match_content[race_number]['Race Horse'][Horse_number]['age'] = horse_horse_age
            #jockey
            jockey_name = horse[7].get_text().strip()
            if jockey_name.find('(') > 0: #jockey has (-XX)
                jockey_name = jockey_name[:jockey_name.find('(')].strip()
            jockey_chi_name = get_jockey_chi_name(jockey_name)
            self.match_content[race_number]['Race Horse'][Horse_number]['jockey'] = jockey_chi_name

            # trainer
            trainer_name = horse[8].get_text().strip()
            trainer_chi_name = get_trainer_chi_name(trainer_name)
            self.match_content[race_number]['Race Horse'][Horse_number]['trainer'] = trainer_chi_name

            ###
            horse_game_history = get_horse_game_history(horse_name)
            ###
            # 'last 6 Runs'
            all_place = []
            for game in horse_game_history:  # loop all the match
                try:
                    place = int(game[1])
                except ValueError:
                    place = 7  # name as 7 if no place
                all_place.append(place)

            while len(all_place) < 6:  # if not enough 6 past game
                all_place.append(7)  # name as 7 for that match

            last_6_place = all_place[:6]
            self.match_content[race_number]['Race Horse'][Horse_number]['last 6 Runs'] = last_6_place

            # 'same distance game result'
            same_distance = get_result_by_distance(horse_game_history, int(race_distance), self.match_place[-1], self.match_content[race_number]['Race Info'][2])
            self.match_content[race_number]['Race Horse'][Horse_number]['same distance game result'] = same_distance

            # class change
            game_history_class, class_change = get_class_change(horse_game_history, race_class)
            self.match_content[race_number]['Race Horse'][Horse_number]['class change'] = class_change
            self.match_content[race_number]['Race Horse'][Horse_number]['game_history_class'] = game_history_class


            # last game date
            last_game_date, last_game_days_delta, status = get_hourse_condition(horse_game_history, self.match_date)
            self.match_content[race_number]['Race Horse'][Horse_number]['last game date'] = last_game_date
            self.match_content[race_number]['Race Horse'][Horse_number]['last game date delta'] = last_game_days_delta
            self.match_content[race_number]['Race Horse'][Horse_number]['status'] = status



    def closed(self, reason):
        #print (self.match_content.keys())
        total_race = len(self.match_content.keys()) - 2
        print (total_race)
        #pprint.pprint(self.match_content)
        print('Spider ended:', reason)

        with open('recent_match.csv', 'w') as recent_csv:
            wr = csv.writer(recent_csv, quoting=csv.QUOTE_ALL)
            heeder_row = ['' for i in range(11)]
            heeder_row += ['Match Date:', self.match_content['match_date'],'','Match Place:', self.match_content['match_place']]
            #wr.writerow(heeder_row)
            #wr.writerow([])
            for race_num in range(1, total_race+1):
                race_key = 'Race {}'.format(race_num)
                race_row = ['' for i in range(11)] + [race_key]
                #wr.writerow(race_row)

                match_date = self.match_content['match_date']
                match_course = ''
                if self.match_content[race_key]['Race Info'][2] == 'ALL WEATHER TRACK':
                    match_course = '田泥'
                else:
                    if self.match_content['match_place'][-1] == 'sha tin':
                        match_course = '田草'
                    if self.match_content['match_place'][-1] == 'happy valley':
                        match_course = '谷草'
                match_class = self.match_content[race_key]['Race Info'][1]
                match_distance = self.match_content[race_key]['Race Info'][4]
                track = self.match_content[race_key]['Race Info'][3]


                match_info = ['' for i in range(11)] + ['Match Time:', match_date,
                                                        '',
                                                        '班次:', match_class,
                                                        '',
                                                        '跑道:', self.match_content[race_key]['Race Info'][2],
                                                        '',
                                                        '賽道:', track,
                                                        '',
                                                        '賽程:', match_distance,
                                                        ]
                #wr.writerow(match_info)

                wr.writerow (['日期', '場次', '跑道', '班次', '路程', '賽道', '場地狀況', '預計步速', '預計疊數', '預計跑法', '評分優勢',
                              '馬號', '王牌', '優先', '檔位', '馬名', '馬齡', '騎師', '練馬師',
                              'last game 1', 'last game 2', 'last game 3', 'last game 4', 'last game 5', 'last game 6',
                              '同路程次數', '同路程冠', '同路程亞', '同路程季', '同路程殿',
                              '上場班次','兩場前班次','三場次班次','升/降班', '上次比賽日', '離上次比賽日數', '狀態'
                              ])

                horse_number = 0 # ensure the hourse number will be in order 1 - 14


                for horse_num, horse_detail in self.match_content[race_key]['Race Horse'].items():
                    horse_number += 1
                    horse_row = [match_date, race_key, match_course, match_class, match_distance, track]
                    for i in range(5):
                        horse_row.append('')
                    if horse_num != horse_number:
                        horse_row.append(horse_number)
                    else:
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

                    wr.writerow(horse_row)

                while horse_number <= 14: # less than 14 horse
                    horse_row = [match_date, race_key, match_course, match_class, match_distance, track]
                    for i in range(5):
                        horse_row.append('')
                    horse_row.append(horse_number)
                    wr.writerow(horse_row)
                    horse_number += 1



                #wr.writerow([])




        #pprint.pprint(self.match_content)

        #
        # ###############
        # ### testing ###
        # ###############
        # tmp_horse = all_horse[-3]
        # tmp_horse = BeautifulSoup(tmp_horse, "html.parser")
        # tmp_horse_all_data = tmp_horse.select("td[class*='tableContent']")
        #
        # #Draw if no draw then skip it
        # skip_row = False
        # horse_draw = tmp_horse_all_data[4].get_text().strip()
        # try:
        #     horse_draw = int(horse_draw)
        #     self.match_content[race_number]['draw'] = horse_draw
        # except ValueError:
        #     skip_row = True
        #
        # #number
        # Horse_number = tmp_horse_all_data[1].get_text()
        # try:
        #     Horse_number = int(Horse_number)
        # except:
        #     pass
        # self.match_content[race_number]['Race Horse']['number'] = Horse_number
        #
        # #Horse Name, Horse Chi Name
        # horse_name = tmp_horse_all_data[3].get_text().strip()
        # horse_chi_name =get_horse_chi_name(horse_name)
        # self.match_content[race_number]['Race Horse']['name'] = horse_chi_name
        #
        # #jockey
        # jockey_name = tmp_horse_all_data[6].get_text().strip()
        # if jockey_name.find('(') > 0: #jockey has (-XX)
        #     jockey_name = jockey_name[:jockey_name.find('(')].strip()
        # print (jockey_name)
        # jockey_chi_name = get_jockey_chi_name(jockey_name)
        # self.match_content[race_number]['Race Horse']['jockey'] = jockey_chi_name
        #
        # #trainer
        # trainer_name = tmp_horse_all_data[7].get_text().strip()
        # trainer_chi_name = get_trainer_chi_name(trainer_name)
        # self.match_content[race_number]['Race Horse']['trainer'] = trainer_chi_name
        #
        # ###
        # horse_game_history = get_horse_game_history(horse_name)
        # ###
        # #'last 6 Runs'
        # all_place = []
        # for game in horse_game_history: # loop all the match
        #     try:
        #         place = int(game[1])
        #     except ValueError:
        #         place = 7 #name as 7 if no place
        #     all_place.append(place)
        #
        # while len(all_place)< 6: #if not enough 6 past game
        #     all_place.append(7) #name as 7 for that match
        #
        # last_6_place = all_place[:6]
        # self.match_content[race_number]['Race Horse']['last 6 Runs'] = last_6_place
        #
        # #'same distance game result'
        # same_distance = get_result_by_distance(horse_game_history, int(race_distance))
        # self.match_content[race_number]['Race Horse']['same distance game result'] = same_distance
        #
        # # class change
        # class_change = get_class_change(horse_game_history, race_class)
        # self.match_content[race_number]['Race Horse']['class change'] = class_change
        #
        #
        # pprint.pprint (self.match_content)



