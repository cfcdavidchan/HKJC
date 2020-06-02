import scrapy
from HKJC_crawler.items import DrawstatisticsItem
from bs4 import BeautifulSoup

class DrawCrawler(scrapy.Spider):

    name = 'Draw_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/information/Chinese/Racing/DrawAdvSearch.aspx/?Year=2017']
    # first input place e.g. 'STT' 田草/ 'STA' 田泥 / 'HVT' 谷草
    # second input course e.g. A / A%2%B
    # third input distance e.g. 1000 / 1200

    def __init__(self):
        self.Draw_option = {'田草':
                           {'1000':
                                {'A': ['STT', 'A', '1000'],
                                 'A+2': ['STT', 'A%2B2', '1000'],
                                 'A+3': ['STT', 'A%2B3', '1000'],
                                 'B': ['STT', 'B', '1000'],
                                 'B+2': ['STT', 'B%2B2', '1000'],
                                 'C': ['STT', 'C', '1000'],
                                 'C+3': ['STT', 'C%2B3', '1000'],
                                 },
                            '1200':
                                {'A': ['STT', 'A', '1200'],
                                 'A+2': ['STT', 'A%2B2', '1200'],
                                 'A+3': ['STT', 'A%2B3', '1200'],
                                 'B': ['STT', 'B', '1200'],
                                 'B+2': ['STT', 'B%2B2', '1200'],
                                 'C': ['STT', 'C', '1200'],
                                 'C+3': ['STT', 'C%2B3', '1200'],
                                 },
                            '1400':
                                {'A': ['STT', 'A', '1400'],
                                 'A+2': ['STT', 'A%2B2', '1400'],
                                 'A+3': ['STT', 'A%2B3', '1400'],
                                 'B': ['STT', 'B', '1400'],
                                 'B+2': ['STT', 'B%2B2', '1400'],
                                 'C': ['STT', 'C', '1400'],
                                 'C+3': ['STT', 'C%2B3', '1400'],
                                 },
                            '1600':
                                {'A': ['STT', 'A', '1600'],
                                 'A+2': ['STT', 'A%2B2', '1600'],
                                 'A+3': ['STT', 'A%2B3', '1600'],
                                 'B': ['STT', 'B', '1600'],
                                 'B+2': ['STT', 'B%2B2', '1600'],
                                 'C': ['STT', 'C', '1600'],
                                 'C+3': ['STT', 'C%2B3', '1600'],
                                 },
                            '1800':
                                {'A': ['STT', 'A', '1800'],
                                 'A+2': ['STT', 'A%2B2', '1800'],
                                 'A+3': ['STT', 'A%2B3', '1800'],
                                 'B': ['STT', 'B', '1800'],
                                 'B+2': ['STT', 'B%2B2', '1800'],
                                 'C': ['STT', 'C', '1800'],
                                 'C+3': ['STT', 'C%2B3', '1800'],
                                 },
                            '2000':
                                {'A': ['STT', 'A', '2000'],
                                 'A+2': ['STT', 'A%2B2', '2000'],
                                 'A+3': ['STT', 'A%2B3', '2000'],
                                 'B': ['STT', 'B', '2000'],
                                 'B+2': ['STT', 'B%2B2', '2000'],
                                 'C': ['STT', 'C', '2000'],
                                 'C+3': ['STT', 'C%2B3', '2000'],
                                 },
                            '2200':
                                {'A': ['STT', 'A', '2200'],
                                 'A+2': ['STT', 'A%2B2', '2200'],
                                 'A+3': ['STT', 'A%2B3', '2200'],
                                 'B': ['STT', 'B', '2200'],
                                 'B+2': ['STT', 'B%2B2', '2200'],
                                 'C': ['STT', 'C', '2200'],
                                 'C+3': ['STT', 'C%2B3', '2200'],
                                 },
                            '2400':
                                {'A': ['STT', 'A', '2400'],
                                 'A+2': ['STT', 'A%2B2', '2400'],
                                 'A+3': ['STT', 'A%2B3', '2400'],
                                 'B': ['STT', 'B', '2400'],
                                 'B+2': ['STT', 'B%2B2', '2400'],
                                 'C': ['STT', 'C', '2400'],
                                 'C+3': ['STT', 'C%2B3', '2400'],
                                 },
                            },
                       '田泥':
                           {'1200':
                                ['STA', '1200'],
                            '1650':
                                ['STA', '1650'],
                            '1800':
                                ['STA', '1800'],
                                 },
                       '谷草':
                           {'1000':
                                {'A': ['HVT', 'A', '1000'],
                                 'A+2': ['HVT', 'A%2B2', '1000'],
                                 'A+3': ['HVT', 'A%2B3', '1000'],
                                 'B': ['HVT', 'B', '1000'],
                                 'B+2': ['HVT', 'B%2B2', '1000'],
                                 'C': ['HVT', 'C', '1000'],
                                 'C+3': ['HVT', 'C%2B3', '1000'],
                                 },
                            '1200':
                                {'A': ['HVT', 'A', '1200'],
                                 'A+2': ['HVT', 'A%2B2', '1200'],
                                 'A+3': ['HVT', 'A%2B3', '1200'],
                                 'B': ['HVT', 'B', '1200'],
                                 'B+2': ['HVT', 'B%2B2', '1200'],
                                 'C': ['HVT', 'C', '1200'],
                                 'C+3': ['HVT', 'C%2B3', '1200'],
                                 },
                            '1650':
                                {'A': ['HVT', 'A', '1650'],
                                 'A+2': ['HVT', 'A%2B2', '1650'],
                                 'A+3': ['HVT', 'A%2B3', '1650'],
                                 'B': ['HVT', 'B', '1650'],
                                 'B+2': ['HVT', 'B%2B2', '1650'],
                                 'C': ['HVT', 'C', '1650'],
                                 'C+3': ['HVT', 'C%2B3', '1650'],
                                 },
                            '1800':
                                {'A': ['HVT', 'A', '1800'],
                                 'A+2': ['HVT', 'A%2B2', '1800'],
                                 'A+3': ['HVT', 'A%2B3', '1800'],
                                 'B': ['HVT', 'B', '1800'],
                                 'B+2': ['HVT', 'B%2B2', '1800'],
                                 'C': ['HVT', 'C', '1800'],
                                 'C+3': ['HVT', 'C%2B3', '1800'],
                                 },
                            '2200':
                                {'A': ['HVT', 'A', '2200'],
                                 'A+2': ['HVT', 'A%2B2', '2200'],
                                 'A+3': ['HVT', 'A%2B3', '2200'],
                                 'B': ['HVT', 'B', '2000'],
                                 'B+2': ['HVT', 'B%2B2', '2200'],
                                 'C': ['HVT', 'C', '2200'],
                                 'C+3': ['HVT', 'C%2B3', '2200'],
                                 },
                            },
                       }

    def parse(self, response):
        for place, distance_detail in self.Draw_option.items():
            self.place = place
            for distance, course_detail in distance_detail.items():
                self.distance = distance
                if self.place == '田泥':
                    self.course = 'NA'
                    place_key = '&Racecourse={}'.format(course_detail[0])
                    distance_key = '&Distance={}'.format(course_detail[1])
                    url = self.start_urls[0] + place_key + distance_key + '&Going=ALL'

                    yield scrapy.Request(url, callback=self.draw_detail)

                else:
                    for course, api_key in course_detail.items():
                        self.course = course
                        place_key = '&Racecourse={}'.format(api_key[0])
                        course_key = '&Course={}'.format(api_key[1])
                        distance_key = '&Distance={}'.format(api_key[2])
                        url = self.start_urls[0] + place_key + course_key + distance_key + '&Going=ALL'

                        yield scrapy.Request(url, callback=self.draw_detail)

    def draw_detail(self, response):
        url = response.url

        if '&Racecourse={}'.format('STA') in url:
            race_place = '田泥'
            course = 'NA'
            distance_pointer = url.find('&Distance=') + len('&Distance=')

            distance = url[distance_pointer: distance_pointer+ len('0000')]

        else:
            race_place_pointer = url.find('&Racecourse=') + len('&Racecourse=')
            race_api = url[race_place_pointer:race_place_pointer + len('xxx')]
            if race_api == 'STT':
                race_place = '田草'
            if race_api == 'HVT':
                race_place = '谷草'

            distance_pointer = url.find('&Distance=') + len('&Distance=')
            distance = url[distance_pointer: distance_pointer + len('0000')]

            course_pointer_start = url.find('&Course=') + len('&Course=')
            course_pointer_end = url.find('&Distance=')
            course_api = url[course_pointer_start: course_pointer_end]
            if course_api == 'A':
                course = 'A'
            if course_api == 'A%2B2':
                course = 'A+2'
            if course_api == 'A%2B3':
                course = 'A+3'
            if course_api == 'B':
                course = 'B'
            if course_api == 'B%2B2':
                course = 'B+2'
            if course_api == 'C':
                course = 'C'
            if course_api == 'C%2B3':
                course = 'C+3'

        print ('\n\n\n\n\n\n\n')

        table = response.xpath('//tbody[@class= "f_ffxxm"]').extract_first()
        table_soup = BeautifulSoup(table, "html.parser")
        for row in table_soup.find_all('tr'):
            row_detail = row.find_all('td')
            row_item = DrawstatisticsItem()

            draw = row_detail[0].text
            number_game = row_detail[1].text
            number_first = row_detail[2].text
            number_second = row_detail[3].text
            number_third = row_detail[4].text
            number_fourth = row_detail[5].text

            row_item['race_place'] = race_place
            row_item['distance'] = distance
            row_item['course'] = course
            row_item['draw'] = draw
            row_item['number_game'] = number_game
            row_item['number_first'] = number_first
            row_item['number_second'] = number_second
            row_item['number_third'] = number_third
            row_item['number_fourth'] = number_fourth

            yield row_item








