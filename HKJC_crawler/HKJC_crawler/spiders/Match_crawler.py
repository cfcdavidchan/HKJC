import scrapy
from HKJC_crawler.items import MatchInfoItem, MatchResultItem
from HKJC_database.models import Match_Info, Horse_Info, Jockey_Info
from bs4 import BeautifulSoup
import requests
from datetime import datetime


class HorseCrawler(scrapy.Spider):

    name = 'Match_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/information/english/Racing/LocalResults.aspx/']

    def parse(self, response):
        all_match_date = response.xpath('//select[@id="selectId"]/option/@value').extract()
        match_date_list = []
        for date in all_match_date:
            datetime_object = datetime.strptime(date, '%d/%m/%Y')
            string_object = datetime.strftime(datetime_object, '%Y/%m/%d')
            match_date_list.append(string_object)
        print ('All Match Date')
        print (match_date_list)
        # loop the match date
        for match_date in match_date_list:
            match_url = 'https://racing.hkjc.com/racing/information/english/Racing/LocalResults.aspx/?RaceDate=' + match_date
            testing = requests.get(match_url).content
            if b'Cookies must be enabled in order to view this page.' not in testing:
                yield scrapy.Request (match_url, callback=self.match_race_number)
        ## testing ##
        #
        # match_url = 'https://racing.hkjc.com/racing/information/english/Racing/LocalResults.aspx/?RaceDate=' + match_date_list[1]
        # match_url = 'https://racing.hkjc.com/racing/information/english/Racing/LocalResults.aspx/?RaceDate=2019/11/03'
        # yield scrapy.Request(match_url, callback=self.match_race_number)

    def match_race_number(self, response):
        all_race = response.xpath('//table[@class="f_fs12 f_fr js_racecard"]/tr').extract_first()
        all_race_soup = BeautifulSoup(all_race, "html.parser")
        all_race_link = [a['href'] for a in all_race_soup.find_all('a', href=True)]
        race_1_link = all_race_link[0][:-1] + '1'
        all_race_link.insert(0, race_1_link)
        # loop all the match
        for match in all_race_link:
            match_pointer = match.find('aspx') + len('aspx')
            match_url = match[:match_pointer] + '/' + match[match_pointer:]
            match_url = 'https://racing.hkjc.com/' + match_url
            yield scrapy.Request(match_url, callback=self.match_detail)

        # testing ##
        # match = all_race_link[6]
        # match_pointer = match.find('aspx') + len('aspx')
        # match_url = match[:match_pointer] + '/' + match[match_pointer:]
        # match_url = 'https://racing.hkjc.com/' + match_url
        # yield scrapy.Request(match_url, callback=self.match_detail)

    def match_detail(self, response):
        print ('\n\n\n\n')
        print ('In match Detail:')
        print (response.request.url)
        match_info = MatchInfoItem()
        match_info['match_date'] = '' #datefield
        match_info['match_place'] = ''
        match_info['race_number'] = 0
        match_info['distance_M'] = 0
        match_info['match_class'] = ''
        match_info['match_name'] = ''
        match_info['match_prize'] = 0.0
        match_info['match_going'] = ''
        match_info['match_course'] = ''

        #match_date
        try:
            hkjc_api_key_Race = 'RaceDate='
            Race_Begin_point = response.request.url.find(hkjc_api_key_Race) + len(hkjc_api_key_Race)
            Race_end_point = response.request.url.find('&', Race_Begin_point)
            match_date = response.request.url[Race_Begin_point:Race_end_point]
            match_date = datetime.strptime(match_date, '%Y/%m/%d')
            match_info['match_date'] = match_date
        except:
            pass

        #match_place
        #match_place[contains(text(), "Season Stakes")]
        match_place = response.xpath('//td/span[@style="color:#666666;font-size:12px;font-weight:700;font-family:Arial,Verdana,Helvetica,sans-serif;"]/text()').extract_first().strip()
        match_place = match_place.replace(':','').lower()
        match_info['match_place'] = match_place

        #race_number
        try:
            hkjc_api_key_no = 'RaceNo='
            key_no_point = response.request.url.find(hkjc_api_key_no) + len(hkjc_api_key_no)
            race_number = response.request.url[key_no_point:]
            match_info['race_number'] = race_number
        except:
            pass

        #distance_M, match_class
        try:
            class_distance = response.xpath('//tr/td[@style="width: 385px;"]/text()').extract_first().split('-')
            match_class, distance_M = class_distance[0].strip(), class_distance[1].strip()
            match_info['distance_M'] = int(distance_M.replace('M', ''))
            match_info['match_class'] = match_class.lower()
        except:
            pass

        #match_name
        try:
            match_name =response.xpath('//tr/td[contains(text(), "Course :")]/preceding-sibling::td/text()').extract_first().strip()
            match_info['match_name'] = match_name
        except:
            pass

        #match_prize
        try:
            match_prize = response.xpath('//tr/td[contains(text(), "HK$")]/text()').extract_first().strip()
            match_info['match_prize'] = float(match_prize.replace('HK$', '').replace(',',''))
        except:
            pass
        #match_going
        match_going = response.xpath('//tr/td[contains(text(), "Going :")]/following-sibling::td/text()').extract_first().strip().lower()
        match_info['match_going'] = match_going

        #match_course
        match_course = response.xpath('//tr/td[contains(text(), "Course :")]/following-sibling::td/text()').extract_first().strip().lower()
        match_info['match_course'] = match_course
        yield match_info

        print ('\n\n\n')
        print ('Match Result:')
        # match
        match = Match_Info.objects.get(match_date= match_date,
                                       race_number= race_number
                                       )
        #result_table
        result_table = response.xpath('//div[contains(@class, "performance")]').extract_first()
        result_table = BeautifulSoup(result_table, "html.parser")
        result_table = result_table.find_all('tr')[1:]

        # loop the table
        for result_row in result_table:
            result = result_row.find_all('td')

            match_result = MatchResultItem() #init MatchResultItem
            match_result['match'] = match  # foreignkey from Match_Info
            match_result['horse_place'] = ''
            match_result['horse_no'] = None
            match_result['horse'] = None  # foreignkey from Horse_Info
            match_result['jockey'] = None  # foreignkey from Jockey_Info
            match_result['actual_weight'] = 0
            match_result['declar_weight'] = 0
            match_result['draw'] = 0
            match_result['finish_time'] = ''
            match_result['win_odds'] = 0.0

            #horse_place
            try:
                horse_place = result[0].get_text()
                match_result['horse_place'] = horse_place
            except:
                pass

            #horse_no
            try:
                horse_no = int(result[1].get_text().strip())
                match_result['horse_no'] = horse_no
            except:
                pass

            #horse
            try:
                horse = result[2].find('a').get('href')
                horse_api_key = 'HorseId='
                horse = horse[len(horse_api_key)+horse.find(horse_api_key):]
                print (horse)
                horse = Horse_Info.objects.get(hkjc_id= horse)
                match_result['horse'] = horse
            except:
                pass

            #jockey
            try:
                jockey = result[3].find('a').get('href')
                jockey_api_key = 'JockeyId='
                jockey = jockey[len(jockey_api_key)+jockey.find(jockey_api_key): jockey.find('&')]
                jockey = Jockey_Info.objects.get(hkjc_id= jockey)
                match_result['jockey'] = jockey
            except:
                pass

            #actual_weight
            try:
                actual_weight = int(result[5].get_text().strip())
                match_result['actual_weight'] = actual_weight
            except:
                pass

            #declar_weight
            try:
                declar_weight = int(result[6].get_text().strip())
                match_result['declar_weight'] = declar_weight
            except:
                pass

            #draw
            try:
                draw = int(result[7].get_text().strip())
                match_result['draw'] = draw
            except:
                pass

            #finish_time
            try:
                finish_time = result[10].get_text().strip()
                match_result['finish_time'] = finish_time
            except:
                pass

            #win_odds
            try:
                win_odds = float(result[11].get_text().strip())
                match_result['win_odds'] = win_odds
            except:
                pass

            yield match_result

