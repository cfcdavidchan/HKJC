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

    def get_sheet_last_row_number(self, sheet_index):
        target_sheet = self.worksheets.get_worksheet(sheet_index)
        a_column = target_sheet.col_values(col=1, value_render_option='FORMULA')
        return len(a_column)

    def get_every_row(self, sheet_index):
        target_sheet = self.worksheets.get_worksheet(sheet_index)
        all_row_data = []
        total_row = target_sheet.row_count
        return target_sheet.get_all_values()





    def write_at_last_row(self, sheet_index, data):
        #get into the target sheet
        target_sheet = self.worksheets.get_worksheet(sheet_index)
        data.insert(0, [])
        #get last row number
        last_row_number = self.get_sheet_last_row_number(sheet_index= sheet_index)
        #writing the data into the sheet
        target_sheet.update('A%d'%last_row_number, data, value_input_option='USER_ENTERED')


    def update_cell(self, sheet_index, row, column, data):

        target_sheet = self.worksheets.get_worksheet(sheet_index)
        target_sheet.update_cell(row= row, col= column, value=data)

    def update_multi_cells(self,sheet_index, data):
        '''

        :param sheet_index:
        :param data: Cell Object from gspread.models
        :return:
        '''

        target_sheet = self.worksheets.get_worksheet(sheet_index)
        target_sheet.update_cells(data)

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







import os, sys, csv
base_path = sys.path[0] # obtain the path of this directory
project_path = os.path.abspath(os.path.join(base_path, '../'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','HKJC.settings')
import django
django.setup()

#from ..HKJC_database.models import Jockey_Info, Trainer_Info, Horse_Info, Match_Result, Jockey_Report
from HKJC_database.models import Jockey_Info, Jockey_Report, Trainer_Info, Trainer_Report, Match_Result, Draw_statistics, Horse_Info
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

def get_trainerXjockey_rate():
    # get all trainer chinese name
    all_trainer = Trainer_Info.objects.all()
    all_trainer_chi_name = [trainer.chinese_name for trainer in all_trainer]

    # get all jockey chinese name
    all_jockey = Jockey_Info.objects.all()
    all_jockey_chi_name = [jockey.chinese_name for jockey in all_jockey]

    result_dict = dict()

    for trainer in all_trainer:
        trainer_id = trainer.id
        trainer_chi_name = trainer.chinese_name

        result_dict[trainer_chi_name] = dict()

        for jockey in all_jockey:
            jockey_id = jockey.id
            jockey_chi_name = jockey.chinese_name

            result_dict[trainer_chi_name][jockey_chi_name] =dict()
            result_dict[trainer_chi_name][jockey_chi_name]['number of game'] = int()
            result_dict[trainer_chi_name][jockey_chi_name]['in place'] = [] # number_win, win_rate
            result_dict[trainer_chi_name][jockey_chi_name]['in win'] = []  # number_place, place_rate

            #count number of game
            number_game = len(Match_Result.objects.filter(trainer_id= trainer.id, jockey_id= jockey_id))
            result_dict[trainer_chi_name][jockey_chi_name]['number of game'] = number_game

            #count number of win
            number_win = len(Match_Result.objects.filter(trainer_id= trainer.id, jockey_id= jockey_id, horse_place= 1))
            if number_game == 0:
                win_rate = 0
            else:
                win_rate = number_win/number_game

            result_dict[trainer_chi_name][jockey_chi_name]['in win'] = [number_win, win_rate]

            #count number of win
            number_place = len(Match_Result.objects.filter(trainer_id= trainer.id, jockey_id= jockey_id, horse_place__in= [1,2,3]))
            if number_game == 0:
                place_rate = 0
            else:
                place_rate = number_place/number_game

            result_dict[trainer_chi_name][jockey_chi_name]['in place'] = [number_place, place_rate]

    return result_dict, all_trainer_chi_name, all_jockey_chi_name

import string
def col2num(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def excel_column():
    from string import ascii_uppercase

    b_z = [letter for letter in ascii_uppercase[1:]]

    aa_az = ['A' + letter for letter in ascii_uppercase]
    ba_az = ['B' + letter for letter in ascii_uppercase]
    ca_az = ['C' + letter for letter in ascii_uppercase]
    da_az = ['D' + letter for letter in ascii_uppercase]
    ea_az = ['E' + letter for letter in ascii_uppercase]

    all_column = b_z + aa_az + ba_az + ca_az + da_az + ea_az

    return all_column

def get_recent_match():
    path = os.getcwd()
    project_path = os.path.dirname(path)
    csv_path = os.path.join(project_path, 'HKJC_crawler')
    csv_path = os.path.join(csv_path, 'recent_match.csv')

    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data

def get_Drawstatistics():
    all_draw_data = Draw_statistics.objects.all().values()
    all_draw_data_list = []
    for data in all_draw_data:
        row_data = [data['race_place'], data['distance'], data['course'],
                    data['draw'], data['number_game'],
                    data['number_first'], data['number_second'], data['number_third'], data['number_fourth']]

        all_draw_data_list.append(row_data)

    return all_draw_data_list

def horse_game_result(match_date, race_number, horse_no, horse_chi_name= None):
    horse_place = 0
    win_odds = None
    place_odds = None
    if horse_chi_name != None:
        try:
            result = Match_Result.objects.get(match_id__match_date= match_date, match_id__race_number= race_number, horse_no=horse_no, horse_id__chinese_name=horse_chi_name)
            result = result.__dict__
            horse_place = int(result['horse_place'])
            win_odds = result['win_odds']
            place_odds = result['place_odds']
        except Match_Result.DoesNotExist:
            print ('No related data')

        return horse_place, win_odds, place_odds
    else:
        try:
            result = Match_Result.objects.get(match_id__match_date=match_date, match_id__race_number=race_number, horse_no=horse_no)
            result = result.__dict__
            horse_place = result['horse_place']
            win_odds = result['win_odds']
            place_odds = result['place_odds']
        except Match_Result.DoesNotExist:
            print('No related data')

        return horse_place, win_odds, place_odds

def get_horse_chi_name_from_match(match_date, race_number, horse_no):
    horse_chi_name = None
    try:
        match_result = Match_Result.objects.get(match_id__match_date=match_date, match_id__race_number=race_number, horse_no=horse_no)
        horse_id = match_result.horse_id
    except Match_Result.DoesNotExist:
        print('No related match')
        return None

    try:
        horse = Horse_Info.objects.get(pk= horse_id)
    except Horse_Info.DoesNotExist:
        print (horse_id)
        print('No related horse')
        return None

    try:
        horse_chi_name = horse.chinese_name
    except:
        pass

    return horse_chi_name

if __name__ == '__main__':
    #pprint (get_list_trainer_season_report())
    # horse_place, win_odds = horse_game_result(match_date='2020-05-03', race_number=6, horse_no=1, horse_chi_name='理想回報')
    # print (horse_place, win_odds)
    #get_horse_chi_name_from_match(match_date='2020-05-03', race_number=6, horse_no=1)
    # result_dict, all_trainer_chi_name, all_jockey_chi_name =  get_trainerXjockey_rate()
    # pprint (result_dict)
    pass