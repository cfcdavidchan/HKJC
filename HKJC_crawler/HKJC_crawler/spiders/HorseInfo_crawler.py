import scrapy
from HKJC_database.models import Trainer_Info
from HKJC_crawler.items import HorseInfoItem, HorseReportItem, HorseRankingItem
from bs4 import BeautifulSoup
import requests
from datetime import datetime

class HorseCrawler(scrapy.Spider):

    name = 'Horse_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/information/English/Horse/ListbyStable.aspx/?TrainerId={}']

    def __init__(self):
        self.all_trainer_id = Trainer_Info.objects.values_list('hkjc_id')
        self.all_trainer_id  = [trainer_id[0] for trainer_id in self.all_trainer_id]
        print (self.all_trainer_id)
        print ('number of trainer:', len(self.all_trainer_id))

    def parse(self, response):
        # check trainer
        # trainer_id = 'CAS'
        # trainer_directory = self.start_urls[0].format(trainer_id)
        # yield scrapy.Request(trainer_directory, callback=self.trainer_detail)

        for trainer in self.all_trainer_id:
            trainer_id = trainer
            print ('\n\n\ntrainer id:', trainer_id)
            trainer_directory = self.start_urls[0].format(trainer_id)
            yield scrapy.Request (trainer_directory, callback=self.trainer_detail)

    def trainer_detail(self, response):
        #check whether the trainer has hors
        print ('\n\n\nIn trainer Detail')
        table = response.xpath('//table[@class= "bigborder"]//td[@class="table_eng_text"]/font[@color="#FFFFFF"]/text()').extract_first()
        if table == None: # The Trainer has Horse coz it does't has NIL example:https://racing.hkjc.com/racing/information/english/Horse/ListbyStable.aspx?TrainerId=TY
            # get the target table
            target_link_table = response.xpath('//table[@class= "bigborder"]').extract_first()
            target_link_table = BeautifulSoup(target_link_table, "html.parser")
            # Get all link of each horse
            all_hourse_link = [a['href'] for a in target_link_table.find_all('a', href=True)]
            print (len(all_hourse_link))
            horse_url_base = 'https://racing.hkjc.com'
            for hourse_link in all_hourse_link:
                aspx_position = hourse_link.find('aspx') + len('aspx')
                hourse_link = hourse_link[:aspx_position] + '/' + hourse_link[aspx_position:]

                horse_url = horse_url_base + hourse_link
                yield scrapy.Request(horse_url, callback=self.parseHorsedetail)
        else:
            trainer_id = response.request.url
            hkjc_trainer_api = 'TrainerId='
            trainer_id = trainer_id[trainer_id.find(hkjc_trainer_api)+len(hkjc_trainer_api):]
            print (trainer_id)
            print('The Trainer does not has any horses')
            pass

        # #check horse
        # horse_url = 'https://racing.hkjc.com/racing/information/English/Horse/Horse.aspx/?HorseId=HK_2019_D310'
        # yield scrapy.Request(horse_url, callback=self.parseHorsedetail)

    def parseHorsedetail(self, response):
        # HorseInfoItem field
        horseInfo = HorseInfoItem()
        horseInfo['name'] = ''
        horseInfo['chinese_name'] = ''
        horseInfo['hkjc_id'] = ''
        horseInfo['origin'] = ''
        horseInfo['age'] = 0
        horseInfo['trainer'] = None
        horseInfo['owner'] = ''
        horseInfo['sire'] = ''
        horseInfo['dam'] = ''
        horseInfo['dam_sire'] = ''
        #
        #hkjc_id
        horse_url = response.request.url
        try:
            hkjc_id_api_key = '?HorseId='
            hkjc_id = str(horse_url).find(hkjc_id_api_key)
            hkjc_id = horse_url[hkjc_id+len(hkjc_id_api_key):]
            horseInfo['hkjc_id'] = hkjc_id
        except:
            pass
        #english_name
        try:
            name = response.xpath('//span[@class= "title_text"]/text()').extract_first()
            name = (name[:name.find('(')]).strip()
            horseInfo['name'] = name
        except:
            pass
        # chinese name
        try:
            horse_chi_url = (response.request.url).replace('English', 'Chinese')
            chinese_request = requests.get(horse_chi_url)
            chinese_name = BeautifulSoup(chinese_request.content, "html.parser")
            chinese_name = (chinese_name.find('span', attrs={'class': "title_text"})).text
            chinese_name = (chinese_name[:chinese_name.find('(')]).strip()
            horseInfo['chinese_name'] = chinese_name
        except:
            pass
        #origin/age
        try:
            origin_age = response.xpath('//tr/td[text()="Country of Origin / Age"]/following-sibling::td/following-sibling::td/text()').extract_first()
            origin, age = origin_age.split('/')[0].strip(), int(origin_age.split('/')[1].strip())
            horseInfo['origin'] = origin
            horseInfo['age'] = age
        except:
            pass
        try:
            #trainer
            trainer_id = response.xpath('//tr/td[text()="Trainer"]/following-sibling::td/following-sibling::td/a/@href').extract_first()
            hkjc_trainer_api = 'TrainerId='
            trainer_id = trainer_id[trainer_id.find(hkjc_trainer_api) + len(hkjc_trainer_api):]
            horseInfo['trainer'] = trainer_id
        except:
            pass

        #owner
        try:
            owner = response.xpath('//tr/td[text()="Owner"]/following-sibling::td/following-sibling::td/a/text()').extract_first().strip()
            horseInfo['owner'] = owner
        except:
            pass

        #sire
        try:
            sire = response.xpath('//tr/td[text()="Sire"]/following-sibling::td/following-sibling::td/a/text()').extract_first().strip()
            horseInfo['sire'] = sire
        except:
            pass

        #dam
        try:
            dam = response.xpath('//tr/td[text()="Dam"]/following-sibling::td/following-sibling::td/text()').extract_first().strip()
            horseInfo['dam'] = dam
        except:
            pass

        #dam_sire
        try:
            dam_sire = response.xpath('//tr/td[text()="{}"]/following-sibling::td/following-sibling::td/text()'.format("Dam's Sire")).extract_first().strip()
            horseInfo['dam_sire'] = dam_sire
        except:
            pass

        #HorseReportItem field
        horseReport = HorseReportItem()
        horseReport['horse'] = ''
        horseReport['current_rank'] = 0
        horseReport['season_start_rank'] = 0
        horseReport['season_stakes'] = 0.0
        horseReport['total_stakes'] = 0.0

        #foregin key from horseino
        horseReport['horse'] = hkjc_id
        #current_rank
        try:
            current_rank = response.xpath('//tr/td[text()="Current Rating"]/following-sibling::td/following-sibling::td/text()').extract_first().strip()
            horseReport['current_rank'] = int(current_rank)
        except:
            pass
        #season_start_rank
        try:
            season_start_rank = response.xpath('//tr/td[contains(text(), "Start of")]/following-sibling::td/following-sibling::td/text()').extract_first().strip()
            horseReport['season_start_rank'] = int(season_start_rank)
        except:
            pass
        #season stakes
        try:
            season_stakes = response.xpath('//tr/td[contains(text(), "Season Stakes")]/following-sibling::td/following-sibling::td/text()').extract_first().strip()
            horseReport['season_stakes'] = float(season_stakes.replace(',', '').replace('$', ''))
        except:
            pass
        #total stakes
        try:
            total_stakes = response.xpath('//tr/td[contains(text(), "Total Stakes")]/following-sibling::td/following-sibling::td/text()').extract_first().strip()
            horseReport['total_stakes'] = float(total_stakes.replace(',', '').replace('$', ''))
        except:
            pass


        yield horseInfo
        yield horseReport
        rating_url = 'https://racing.hkjc.com/racing/information/English/Horse/RatingResultWeight.aspx/?HorseId='+ hkjc_id
        yield scrapy.Request(rating_url, callback=self.parseRatingdetail)


    def parseRatingdetail(self, response):
        hkjc_id_api_key = '?HorseId='
        hkjc_id = str(response.request.url).find(hkjc_id_api_key)
        hkjc_id = response.request.url[hkjc_id + len(hkjc_id_api_key):]
        table = response.xpath('//table[@class= "bigborder"]/tr[@bgcolor= "FFFFFF"]').extract()[:2]
        first_row = BeautifulSoup(table[0], "html.parser")
        first_row = [field.get_text() for field in (first_row.find_all('span', attrs={'class': "table_eng_text"}))][1:]
        second_row = BeautifulSoup(table[1], "html.parser")
        second_row = [field.get_text() for field in (second_row.find_all('span', attrs={'class': "table_eng_text"}))][1:]

        for date, rank in zip(first_row, second_row):
            ranking_item = HorseRankingItem()
            date = datetime.strptime(date, '%d/%m/%Y')
            rank = int(rank)

            ranking_item['horse'] = hkjc_id
            ranking_item['rank'] = rank
            ranking_item['rank_reord_date'] = date

            yield ranking_item

