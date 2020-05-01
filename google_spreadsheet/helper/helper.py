import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
from pprint import pprint

class google_sheet_manager():
    def __init__(self, cred_json_path, worksheet_key):
        '''
        :param cred_json_path: the json path of the google cred
        :param worksheet_key: the api key of the weeksheet
        '''
        gss_scopes = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_json_path, gss_scopes)
        gss_client = gspread.authorize(credentials)

        self.worksheets = gss_client.open_by_key(worksheet_key)

    def get_worksheet(self, sheet_index):
        target_sheet = self.worksheets.get_worksheet(sheet_index)
        return target_sheet

    def all_sheet_name_dict(self):
        '''
        :return: a dictionary {sheetname: index}
        '''
        self.all_sheet = {}
        sheets = self.worksheets._spreadsheets_get()['sheets']
        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            sheet_index = sheet['properties']['index']
            self.all_sheet[sheet_name] = sheet_index

        return self.all_sheet

    def clean_and_write(self, sheet_index, data):
        '''
        :param sheet_index: the indext of the target sheet
        :param data: the data in list
        :return:
        '''
        #get into the target sheet
        target_sheet = self.worksheets.get_worksheet(sheet_index)
        #clean the existing value
        target_sheet.clear()
        #writing the data into the sheet
        target_sheet.update('A1', data, value_input_option='USER_ENTERED')







import os, sys
base_path = sys.path[0] # obtain the path of this directory
project_path = os.path.abspath(os.path.join(base_path, '../'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','HKJC.settings')
import django
django.setup()

#from ..HKJC_database.models import Jockey_Info, Trainer_Info, Horse_Info, Match_Result, Jockey_Report
from HKJC_database.models import Jockey_Info, Jockey_Report, Trainer_Info, Trainer_Report
#from ..HKJC_database.models import Jockey_Info, Jockey_Report

def get_list_jockey_season_report():
    season = list(set(Jockey_Report.objects.values_list('season', flat=True)))
    season.sort(reverse=True)
    current_season = season[0]
    previos_season = season[1]

    jockey_season_report = dict()
    all_jockey = Jockey_Report.objects.all()
    #
    for jockey in all_jockey:
        jockey_chi_name = jockey.jockey.chinese_name
        if jockey_chi_name not in jockey_season_report.keys():
            jockey_season_report[jockey_chi_name] = dict()
            jockey_season_report[jockey_chi_name]['current season'] = ['',0,0,0,0,0]
            jockey_season_report[jockey_chi_name]['previos season'] = [0,0,0,0,0]

        season = jockey.season
        total_rides = jockey.total_rides
        number_win = jockey.number_win
        number_second = jockey.number_second
        number_third = jockey.number_third
        number_fourth = jockey.number_fourth

        if season == current_season:
            weight_adv = ''
            jockey_season_report[jockey_chi_name]['current season'] = [weight_adv,
                                                                       total_rides,
                                                                       number_win,
                                                                       number_second,
                                                                       number_third,
                                                                       number_fourth]
        if season == previos_season:
            jockey_season_report[jockey_chi_name]['previos season'] = [total_rides,
                                                                       number_win,
                                                                       number_second,
                                                                       number_third,
                                                                       number_fourth]

    # return List
    result =sorted(jockey_season_report.items(), key=lambda item: item[1]['current season'][1], reverse=True)

    return result

def tarainer_coursereport(url_current_season):
    previous_url = url_current_season.replace('Current', 'Previous')

    trainer_report = dict()
    # Get the current season report
    trainer_current_report = requests.get(url_current_season)
    trainer_soup = BeautifulSoup(trainer_current_report.content, "html.parser")

    all_trainer_table = trainer_soup.findAll('tbody', attrs={'class': "f_tac f_fs12"})
    for table in all_trainer_table:
        table_trainer = table.findAll('tr')
        for trainer in table_trainer:
            try:
                trainer_name = trainer.find('a').get_text()
            except:
                continue

            number_game = trainer.findAll('td')[-1].get_text().strip()
            number_first = trainer.findAll('td')[1].get_text().strip()
            number_second = trainer.findAll('td')[2].get_text()
            number_third = trainer.findAll('td')[3].get_text()
            number_fourth = trainer.findAll('td')[4].get_text()

            if trainer_name not in trainer_report.keys():
                trainer_report[trainer_name] = dict()
                trainer_report[trainer_name]['current season'] = [0, 0, 0, 0, 0]
                trainer_report[trainer_name]['previous season'] = [0, 0, 0, 0, 0]

            trainer_report[trainer_name]['current season'] = [number_game, number_first, number_second, number_third, number_fourth]

    # Get the previos report
    trainer_current_report = requests.get(previous_url)
    trainer_soup = BeautifulSoup(trainer_current_report.content, "html.parser")

    all_trainer_table = trainer_soup.findAll('tbody', attrs={'class': "f_tac f_fs12"})

    for table in all_trainer_table:
        table_trainer = table.findAll('tr')
        for trainer in table_trainer:
            try:
                trainer_name = trainer.find('a').get_text()
            except:
                continue
            number_game = trainer.findAll('td')[-1].get_text().strip()
            number_first = trainer.findAll('td')[1].get_text().strip()
            number_second = trainer.findAll('td')[2].get_text()
            number_third = trainer.findAll('td')[3].get_text()
            number_fourth = trainer.findAll('td')[4].get_text()

            if trainer_name not in trainer_report.keys():
                trainer_report[trainer_name] = dict()
                trainer_report[trainer_name]['current season'] = [0, 0, 0, 0, 0]
                trainer_report[trainer_name]['previous season'] = [0, 0, 0, 0, 0]

            trainer_report[trainer_name]['previous season'] = [number_game, number_first, number_second, number_third, number_fourth]

    return trainer_report

def get_list_trainer_season_report():
    trainer_season_report = dict()
    #沙田草地
    url = 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerRanking.aspx/?Season=Current&View=Numbers&Racecourse=STT'
    ST_Turf = tarainer_coursereport(url)
    #沙田全天侯
    url = 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerRanking.aspx/?Season=Current&View=Numbers&Racecourse=STA'
    ST_Allweather = tarainer_coursereport(url)
    #跑馬地草地
    url = 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerRanking.aspx/?Season=Current&View=Numbers&Racecourse=HVT'
    HV_Turf = tarainer_coursereport(url)

    all_trainer_name = list(set(list(ST_Turf.keys()) + list(ST_Allweather.keys()) + list(HV_Turf.keys())))

    for trainer in all_trainer_name: #Create the return dictionary
        if trainer not in trainer_season_report.keys():
            trainer_season_report[trainer] = dict()
        trainer_season_report[trainer]['沙田草地'] = dict()
        trainer_season_report[trainer]['沙田全天侯'] = dict()
        trainer_season_report[trainer]['跑馬地草地'] = dict()
        # preset as all 0
        trainer_season_report[trainer]['沙田草地']['current season'] = [0, 0, 0, 0, 0]
        trainer_season_report[trainer]['沙田草地']['previous season'] = [0, 0, 0, 0, 0]
        trainer_season_report[trainer]['沙田全天侯']['current season'] = [0, 0, 0, 0, 0]
        trainer_season_report[trainer]['沙田全天侯']['previous season'] = [0, 0, 0, 0, 0]
        trainer_season_report[trainer]['跑馬地草地']['current season'] = [0, 0, 0, 0, 0]
        trainer_season_report[trainer]['跑馬地草地']['previous season'] = [0, 0, 0, 0, 0]

    def fullin_dictioray(season_report, course_dict, course_name):
        for trainer, result in course_dict.items():
            season_report[trainer][course_name] = result
        return season_report

    trainer_season_report = fullin_dictioray(trainer_season_report, ST_Turf, '沙田草地')
    trainer_season_report = fullin_dictioray(trainer_season_report, ST_Allweather, '沙田全天侯')
    trainer_season_report = fullin_dictioray(trainer_season_report, HV_Turf, '跑馬地草地')

    return trainer_season_report


if __name__ == '__main__':
    pprint (get_list_trainer_season_report())