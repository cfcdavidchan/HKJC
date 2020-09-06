import scrapy
from datetime import datetime
import os
import js2xml
from js2xml.utils.vars import get_vars
import csv

class RecentMatchSpider(scrapy.Spider):
    name = 'RealTime_crawler'
    #https: // bet.hkjc.com / racing / pages / odds_wp.aspx?lang = ch & raceno = 7
    start_urls = ['https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=ch&raceno=7']
    def __init__(self, race_number=1, **kwargs):
        self.race_number = str(race_number)
        print ('\n\n\n\n\n')
        print (self.race_number)


        self.start_urls = ['https://bet.hkjc.com/racing/pages/odds_wp.aspx/?lang=ch&raceno={}'.format(self.race_number)]
        super().__init__(**kwargs)

    def parse(self, response):
        self.crawl_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # crawl all horse data
        all_horse = response.xpath('//div[contains(@class,"bodyMainOddsTable content")]/script[contains(@type,"text/javascript")]').extract_first()
        all_horse = all_horse[all_horse.find("var winOddsByRace"):all_horse.rfind("var normalRunnerList")]
        all_horse = all_horse[:all_horse.find(".split")]
        all_horse = get_vars(js2xml.parse(all_horse))
        all_horse = all_horse['winOddsByRace']
        self.odd_dict = dict()
        for i in range(1,15):
            self.odd_dict[i] = [0,0]

            odd_start_str = ";{}=".format((str(i)))
            odd_end_str = "="
            try:
                # win odd
                win_odd = all_horse.find(odd_start_str)
                win_odd_end_pos = all_horse.find(odd_end_str, win_odd+len(odd_start_str))
                win_odd = all_horse[win_odd + len(odd_start_str) : win_odd_end_pos]
                # place odd
                place_odd = all_horse.find(odd_start_str, win_odd_end_pos)
                place_odd = all_horse[place_odd + len(odd_start_str) : all_horse.find(odd_end_str, place_odd + len(odd_start_str))]
                self.odd_dict[i] = [float(win_odd), float(place_odd)]
            except:
                pass

    def close(self):
        directory_path = "RealTime_data"
        today = datetime.now().strftime("%d-%m-%Y")
        csv_path =  os.path.join(directory_path,today)
        csvfile_name = "RealTime_Race{}".format(self.race_number) + ".csv"
        csv_path = os.path.join(csv_path, csvfile_name)
        with open(csv_path, 'a') as realtime_csv:
            wr = csv.writer(realtime_csv, quoting=csv.QUOTE_NONNUMERIC)
            wr.writerow(["Race {}".format(self.race_number), self.crawl_time])
            wr.writerow(['馬號', 'Win', 'Place'])
            for i in range(1, 15):
                win_odd = self.odd_dict[i][0]
                place_odd = self.odd_dict[i][0]
                wr.writerow([str(i), win_odd, place_odd])