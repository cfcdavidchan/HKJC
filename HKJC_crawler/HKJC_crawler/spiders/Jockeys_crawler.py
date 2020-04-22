from HKJC_crawler.items import JockeyItem
import scrapy
import time
import requests
from bs4 import BeautifulSoup
import re

class JockeysSpider(scrapy.Spider):
    name = 'Jockeys_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/information/English/Jockey/JockeyRanking.aspx/']

    def parse(self, response):
        url = self.start_urls[0]
        all_jockeys = response.xpath('//td[@class= "f_fs14 f_tal"]/a/@href').extract()
        print ('start')
        print (all_jockeys)
        print (len(all_jockeys))

        for jockey in all_jockeys:
            aspx_position = jockey.find('aspx') + len('aspx')
            jockey = jockey[:aspx_position] + '/' + jockey[aspx_position:]
            time.sleep(1)
            jockey_url = 'https://racing.hkjc.com' + jockey
            yield scrapy.Request(jockey_url, callback=self.parse_content)

    def parse_content(self, response):
        # Get the url of the request
        url = response.request.url
        # Get the HKJC_id
        hkjc_id_start =url.find('=')+1
        hkjc_id_end = url.find('&', hkjc_id_start)
        hkjc_id = url[hkjc_id_start: hkjc_id_end]
        # Get english name
        try:
            eng_name = response.xpath('//div[@style= "font-size:95%"]').xpath('p[@class= "tit"]/text()').extract_first()
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
            total_rides = response.xpath('//tr/td[text()="Total Rides"]/following-sibling::td/text()').extract_first()
            total_rides = int(re.sub("\D","", total_rides))
        except:
            total_rides = 0

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
            avg_JKC_past_10 = response.xpath('//tr/td[text()="Avg. JKC points in Past 10 race days "]/following-sibling::td/text()').extract_first()
            avg_JKC_past_10 = float(avg_JKC_past_10.replace(':','').replace(',', '').replace('$', ''))
        except:
            avg_JKC_past_10 = 0

        item = JockeyItem()
        item['name'] = eng_name
        item['chinese_name'] = chi_name
        item['hkjc_id'] = hkjc_id
        item['stakes_won'] = stakes_won
        item['wins_past_10_racing'] = wins_past_10_racing
        item['avg_JKC_past_10'] = avg_JKC_past_10
        item['number_win'] = number_win
        item['number_second'] = number_second
        item['number_third'] = number_third
        item['number_fourth'] = number_fourth
        item['total_rides'] = total_rides
        item['win_rate'] = win_rate

        yield item
