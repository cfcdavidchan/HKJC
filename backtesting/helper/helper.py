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

    def create_spreadsheet(self, sheet_name, cols=20, rows= 100):
        try: # Remove the sheet if it is exiting
            target_sheet = self.worksheets.worksheet(sheet_name)
            self.worksheets.del_worksheet(target_sheet)
        except:
            pass
        work_sheet = self.worksheets.add_worksheet(title=sheet_name, cols=cols, rows= rows)

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
