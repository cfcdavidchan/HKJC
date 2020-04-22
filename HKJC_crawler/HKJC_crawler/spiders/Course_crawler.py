import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from .helper.helper import get_chrome_path
#from HKJC_database.models import Going, RacingCourse
from HKJC_crawler.items import CourseItem
from decimal import Decimal
from bs4 import BeautifulSoup
import sys

class CourseCrawler(scrapy.Spider):

    name = 'Course_crawler'
    #allowed_domains = ['racing.hkjc.com']
    start_urls = ['https://racing.hkjc.com/racing/english/racing-info/racing_course.asp']

    def __init__(self):
        # set browser
        chrome_path = get_chrome_path()
        print ('\n\n\n\n\n')
        print (chrome_path)
        print('\n\n\n\n\n')
        self.browser = webdriver.Chrome(chrome_path)
        self.max_retry = 5
        self.current_retry = 0
        # base info from page
        self.course_dict = {'Sha Tin':
                                {'chinese':'沙田',
                                 'english':'sha tin',
                                 },
                            'Happy Valley':
                                {'chinese':'跑馬地',
                                 'english':'happy valley',
                                 },
                            'Conghua':
                                {'chinese':'從化',
                                 'english':'conghua',
                                 },
                            }

        self.going_dict = {'Going (Turf Track)':
                               {'chinese':'草地',
                                'english':'turf'
                                },
                           'Going (All Weather Track)':
                               {'chinese':'全天候',
                                'english':'all weather'
                                },
                           }

    def parse(self, response):
        self.browser.get(response.url)

        sel = Selector(text=self.browser.page_source)
        if self.current_retry < self.max_retry:
            all_table = sel.xpath('//table[@class= "body_text legacyTable"]').extract()
            if len(all_table) == 0:
                self.current_retry += 1
                yield scrapy.Request(response.url, callback=self.parse)
        else:
            print('fail to crawl anything')
            sys.exit()

        for table in all_table:

            table_soup = BeautifulSoup(table, "html.parser")
            try:
                header = table_soup.find('font', attrs={'color': "#FFFFFF"}).text.strip() #extract the header of the table
                header = header.split()
                header = " ".join(header)
                if header in self.course_dict.keys(): #check whether it is a course table
                    chi_name = self.course_dict[header]['chinese']
                    eng_name = self.course_dict[header]['english']
                    all_row = table_soup.find_all('tr', attrs={'valign': "top"})[2:]
                    for row in all_row:  # extract the data from each row
                        item = CourseItem()
                        row_data = row.text.split()
                        course = row_data[1]
                        home_straight = float(row_data[-2].replace('M', ''))
                        width = float(row_data[-1].replace('M', ''))
                        # store it to database
                        item['place'] = eng_name
                        item['chinese_place'] = chi_name
                        item['course'] = course
                        item['home_straight_M'] = home_straight
                        item['width_M'] = width
                        yield item

                # if header in self.going_dict.keys(): #check whether it is a going table
                #     chi_track = self.going_dict[header]['english']
                #     eng_track = self.going_dict[header]['chinese']
                #     all_row = table_soup.find_all('tr', attrs={'valign': "top"})[2:]
                #     for row in all_row:  # extract the data from each row
                #         item = GoingItem()
                #         row_data = row.text.split()
                #         course = row_data[1]
                #         home_straight = float(row_data[-2].replace('M', ''))
                #         width = float(row_data[-1].replace('M', ''))
                #         # store it to database
                #         item['place'] = eng_name
                #         item['chinese_place'] = chi_name
                #         item['course'] = course
                #         item['home_straight_M'] = home_straight
                #         item['width_M'] = width
                #         yield item

            except:
                pass


        print('\n\n\n')
