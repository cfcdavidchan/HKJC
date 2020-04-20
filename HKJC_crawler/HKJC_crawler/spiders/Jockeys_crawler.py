from HKJC_crawler.items import JockeyItem
import scrapy
import time
import requests
from bs4 import BeautifulSoup


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

        # print the result
        item = JockeyItem()
        item['name'] = eng_name
        item['chinese_name'] = chi_name
        item['hkjc_id'] = hkjc_id

        yield item
