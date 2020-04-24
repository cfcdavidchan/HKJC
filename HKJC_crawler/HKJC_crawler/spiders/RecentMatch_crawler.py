import scrapy
from datetime import datetime
from bs4 import BeautifulSoup
import pprint
import csv
from datetime import date
from datetime import date

from .helper.helper import get_horse_chi_name, get_jockey_chi_name, get_trainer_chi_name, get_horse_game_history, get_result_by_distance, get_class_change, get_hourse_condition

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
        self.match_place = match_info[-1]

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
        race_course = race_info[9].replace(',','').lower().strip()
        race_distance = race_info[-1].replace(',','').lower().replace('m','').strip()
        self.match_content[race_number]['Race Info'] = [race_time, race_class, race_course,race_distance]
        self.match_content[race_number]['Race Horse'] = dict()
        #Race Horse
        all_horse = response.xpath('//tr[contains(@height, "22px")]').extract()
        #loop over horse
        for horse in all_horse:
            horse = BeautifulSoup(horse, "html.parser")
            horse = horse.select("td[class*='tableContent']")

            # Draw if no draw then skip it
            skip_row = False
            horse_draw = horse[4].get_text().strip()
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
            # Horse Name, Horse Chi Name
            horse_name = horse[3].get_text().strip()
            horse_chi_name = get_horse_chi_name(horse_name)
            self.match_content[race_number]['Race Horse'][Horse_number]['name'] = horse_chi_name

            #jockey
            jockey_name = horse[6].get_text().strip()
            if jockey_name.find('(') > 0: #jockey has (-XX)
                jockey_name = jockey_name[:jockey_name.find('(')].strip()
            jockey_chi_name = get_jockey_chi_name(jockey_name)
            self.match_content[race_number]['Race Horse'][Horse_number]['jockey'] = jockey_chi_name

            # trainer
            trainer_name = horse[7].get_text().strip()
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
            same_distance = get_result_by_distance(horse_game_history, int(race_distance))
            self.match_content[race_number]['Race Horse'][Horse_number]['same distance game result'] = same_distance

            # class change
            class_change = get_class_change(horse_game_history, race_class)
            self.match_content[race_number]['Race Horse'][Horse_number]['class change'] = class_change

            # last game date
            last_game_date, last_game_days_delta, status = get_hourse_condition(horse_game_history, self.match_date)
            self.match_content[race_number]['Race Horse'][Horse_number]['last game date'] = last_game_date
            self.match_content[race_number]['Race Horse'][Horse_number]['last game date delta'] = last_game_days_delta
            self.match_content[race_number]['Race Horse'][Horse_number]['status'] = status



    def closed(self, reason):
        print (self.match_content.keys())
        total_race = len(self.match_content.keys()) - 2
        print (total_race)
        pprint.pprint(self.match_content)
        print('Spider ended:', reason)

        with open('recent_match.csv', 'w') as recent_csv:
            wr = csv.writer(recent_csv, quoting=csv.QUOTE_ALL)
            wr.writerow(['Match Date:', self.match_content['match_date'],'','Match Place:', self.match_content['match_place']])
            wr.writerow([])
            for race_num in range(1, total_race+1):
                race_key = 'Race {}'.format(race_num)
                wr.writerow([race_key])
                wr.writerow((['Match Time:', self.match_content[race_key]['Race Info'][0],
                              '',
                              '班次:', self.match_content[race_key]['Race Info'][1],
                              '',
                              '跑道:', self.match_content[race_key]['Race Info'][2],
                              '',
                              '賽程:', self.match_content[race_key]['Race Info'][3],
                              ]))

                wr.writerow (['馬號', '檔位', '馬名', '騎師', '練馬師',
                              'last game 1', 'last game 2', 'last game 3', 'last game 4', 'last game 5', 'last game 6',
                              '同路程次數', '同路程冠', '同路程亞', '同路程季', '同路程殿',
                              '升/降班', '上次比賽日', '離上次比賽日數', '狀態'
                              ])

                for horse_num, horse_detail in self.match_content[race_key]['Race Horse'].items():
                    horse_row = [horse_num, horse_detail['draw'], horse_detail['name'],horse_detail['jockey'], horse_detail['trainer']]
                    for place in horse_detail['last 6 Runs']:
                        horse_row.append(place)
                    for result in horse_detail['same distance game result']:
                        horse_row.append(result)
                    horse_row.append(horse_detail['class change'])
                    horse_row.append(horse_detail['last game date'])
                    horse_row.append(horse_detail['last game date delta'])
                    horse_row.append(horse_detail['status'])

                    wr.writerow(horse_row)

                wr.writerow([])




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



