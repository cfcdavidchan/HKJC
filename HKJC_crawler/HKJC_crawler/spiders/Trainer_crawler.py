from HKJC_crawler.items import TrainerInfoItem, TrainerReportItem
import scrapy
import time
import requests
from bs4 import BeautifulSoup
import re

class TrainerSpider(scrapy.Spider):
    name = 'Trainer_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/information/English/Trainers/TrainerRanking.aspx/']

    def parse(self, response):
        url = self.start_urls[0]
        all_trainers = response.xpath('//td[@class= "f_fs14 f_tal"]/a/@href').extract()
        print ('start')
        print (all_trainers)
        print (len(all_trainers))

        for trainer in all_trainers:
            aspx_position = trainer.find('aspx') + len('aspx')
            trainer = trainer[:aspx_position] + '/' + trainer[aspx_position:]
            time.sleep(1)
            current_url = 'https://racing.hkjc.com' + trainer
            previous_url = current_url.replace('Current', 'Previous')
            trainer_url = [current_url, previous_url]
            for url in trainer_url:
                yield scrapy.Request(url, callback=self.parse_content)

    def parse_content(self, response):
        # Get the url of the request
        url = response.request.url

        ##TrainerInfo_item
        # Get the HKJC_id
        hkjc_id_start =url.find('=')+1
        hkjc_id_end = url.find('&', hkjc_id_start)
        hkjc_id = url[hkjc_id_start: hkjc_id_end]
        # Get english name
        try:
            eng_name = response.xpath('//div[@class= "nav f_fs13"]').xpath('p[@class= "tit"]/text()').extract_first()
            eng_name = eng_name.strip().rstrip()
        except:
            eng_name = None
        # Get the Chinese name
        try:
            chinese_url = url.replace('English', 'Chinese')
            chinese_request = requests.get(chinese_url)
            chinese_soup = BeautifulSoup(chinese_request.content, "html.parser")
            chi_name = (chinese_soup.find('div', attrs={'class': "nav f_fs13"}).find('p', attrs={'class': "tit"})).text.strip()
        except:
            chi_name = None



        ## TrainerReport_item
        try:
            season = response.xpath('//td[@colspan= "6"]/text()').extract_first()
            season = season.lower().replace('season','').strip()
        except:
            season = ''
        try:
            number_win = response.xpath('//tr/td[text()="No. of Wins"]/following-sibling::td/text()').extract_first()
            number_win = int(re.sub("\D","", number_win))
        except:
            number_win = 0
        try:
            number_second = response.xpath('//tr/td[text()="No. of 2nds"]/following-sibling::td/text()').extract_first()
            number_second = int(re.sub("\D", "", number_second))
        except:
            number_second = 0

        try:
            number_third = response.xpath('//tr/td[text()="No. of 3rds"]/following-sibling::td/text()').extract_first()
            number_third = int(re.sub("\D", "", number_third))
        except:
            number_third = 0

        try:
            number_fourth = response.xpath('//tr/td[text()="No. of 4ths"]/following-sibling::td/text()').extract_first()
            number_fourth = int(re.sub("\D", "", number_fourth))
        except:
            number_fourth = 0

        try:
            total_runners = response.xpath('//tr/td[text()="Total Runners"]/following-sibling::td/text()').extract_first()
            total_runners = int(re.sub("\D","", total_runners))
        except:
            total_runners = 0

        try:
            win_rate = response.xpath('//tr/td[text()="Win %"]/following-sibling::td/text()').extract_first()
            win_rate = float(win_rate.replace(':','').replace('%', ''))
        except:
            win_rate = 0

        try:
            stakes_won = response.xpath('//tr/td[text()="Stakes won"]/following-sibling::td/text()').extract_first()
            stakes_won = float(stakes_won.replace(':','').replace(',', '').replace('$', ''))
        except:
            stakes_won = 0

        try:
            wins_past_10_racing = response.xpath('//tr/td[text()="No. of Wins in past 10 race days"]/following-sibling::td/text()').extract_first()
            wins_past_10_racing = int(re.sub("\D", "", wins_past_10_racing))
        except:
            wins_past_10_racing = 0


        try:
            url = response.request.url
            stat_url = url.replace('Profile','WinStat')

            trainer_stat = requests.get(stat_url)
            trainer_stat_soup = BeautifulSoup(trainer_stat.content, "html.parser")
            trainer_stat_soup = trainer_stat_soup.find('div', attrs={'class': "performance"}).find('tbody')
            all_td = [i.get_text() for i in trainer_stat_soup.findAll('td')]

            trainer_stat = self.winStat_td_to_dict(all_td)
        except:
            pass
        #print (eng_name)
        #print(chi_name)
        TrainerInfo_item = TrainerInfoItem()
        TrainerInfo_item['name'] = eng_name
        TrainerInfo_item['chinese_name'] = chi_name
        TrainerInfo_item['hkjc_id'] = hkjc_id
        yield TrainerInfo_item

        TrainerReport_item = TrainerReportItem()
        TrainerReport_item['trainer'] = eng_name
        TrainerReport_item['season'] = season
        TrainerReport_item['stakes_won'] = stakes_won
        TrainerReport_item['wins_past_10_racing'] = wins_past_10_racing
        TrainerReport_item['number_win'] = number_win
        TrainerReport_item['number_second'] = number_second
        TrainerReport_item['number_third'] = number_third
        TrainerReport_item['number_fourth'] = number_fourth
        TrainerReport_item['total_runners'] = total_runners
        TrainerReport_item['win_rate'] = win_rate
        TrainerReport_item['win_stat'] = trainer_stat

        yield TrainerReport_item


    def winStat_td_to_dict(self, all_td):
        trainer_win_stat = dict()
        trainer_win_stat[all_td[0].lower().strip()] = dict()  # happy valley
        trainer_win_stat[all_td[0].lower().strip()][int(all_td[1])] = all_td[2:6]  # [win, 2nd, 3rd, total runner]
        trainer_win_stat[all_td[0].lower().strip()][int(all_td[6])] = all_td[7:11]
        trainer_win_stat[all_td[0].lower().strip()][int(all_td[11])] = all_td[12:16]
        trainer_win_stat[all_td[0].lower().strip()][int(all_td[16])] = all_td[17:21]
        trainer_win_stat[all_td[0].lower().strip()][int(all_td[21])] = all_td[22:26]

        trainer_win_stat[all_td[26].lower().strip()] = dict()  # Sha Tin
        trainer_win_stat[all_td[26].lower().strip()][all_td[27].lower().strip()] = dict()  # All Weather
        trainer_win_stat[all_td[26].lower().strip()][all_td[27].lower().strip()][int(all_td[28])] = all_td[29:33]
        trainer_win_stat[all_td[26].lower().strip()][all_td[27].lower().strip()][int(all_td[33])] = all_td[34:38]
        trainer_win_stat[all_td[26].lower().strip()][all_td[27].lower().strip()][int(all_td[38])] = all_td[39:43]

        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()] = dict()  # truf
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[44])] = all_td[45:49]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[49])] = all_td[50:54]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[54])] = all_td[55:59]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[59])] = all_td[60:64]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[64])] = all_td[65:69]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[69])] = all_td[70:74]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[74])] = all_td[75:79]
        trainer_win_stat[all_td[26].lower().strip()][all_td[43].lower().strip()][int(all_td[79])] = all_td[80:84]

        trainer_win_stat[all_td[84].lower().strip()] = dict()  # Conghua
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[85])] = all_td[86:90]
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[90])] = all_td[91:95]
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[95])] = all_td[96:100]
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[100])] = all_td[101:105]
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[105])] = all_td[106:110]
        trainer_win_stat[all_td[84].lower().strip()][int(all_td[110])] = all_td[111:115]

        trainer_win_stat['total'] = all_td[116:121]

        return trainer_win_stat