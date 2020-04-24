import sys, os
from datetime import date, datetime

base_path = os.path.realpath(__file__)
base_path = os.path.dirname(base_path)
global chrome_path
chrome_path = os.path.join(base_path, 'chromedriver')

def get_chrome_path():
    return chrome_path

if __name__ == "main":
    pass

##Obtain django data

# base_path = sys.path[0] # obtain the path of this directory
# project_path = os.path.abspath(os.path.join(base_path, '../../'))
# sys.path.append(project_path)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE','HKJC.settings')
# import django
# django.setup()

from HKJC_database.models import Jockey_Info, Trainer_Info, Horse_Info, Match_Result
from django.forms.models import model_to_dict

def get_horse_chi_name(horse_english_name):
    try:
        horse = Horse_Info.objects.get(name=horse_english_name)
        return horse.chinese_name
    except Horse_Info.DoesNotExist:
        return None

def get_jockey_chi_name(jockey_english_name):
    try:
        jockey = Jockey_Info.objects.get(name=jockey_english_name)
        return jockey.chinese_name
    except Jockey_Info.DoesNotExist:
        return None

def get_trainer_chi_name(trainer_english_name):
    try:
        trainer = Trainer_Info.objects.get(name=trainer_english_name)
        return trainer.chinese_name
    except Trainer_Info.DoesNotExist:
        return None

def get_horse_game_history(horse_name):
    '''
    :param horse_name:
    :return:  [[match_date, place, distance of game, class of the game]]
    '''
    game_history = []
    try:
        horse = Horse_Info.objects.get(name__contains=horse_name)

        match_result = Match_Result.objects.filter(horse=horse)
        for result in match_result: #loop over all tge game
            match_date = result.match.match_date
            place = result.horse_place
            race_distance = result.match.distance_M
            game_class = result.match.match_class
            game_data = [match_date, place, race_distance,game_class]

            game_history.append(game_data)
    except:
        pass

    def sort_date(elem):
        return elem[0]
    game_history.sort(key=sort_date, reverse=True) # sort the result by date
    return game_history


def get_result_by_distance(list_game_game_history, race_distance):
    '''
    :param list_game_game_history: [[match_date, place, distance of game], ...]
    :return: [number of game, number of No.1, number of No.2, number of No.3, number of No.4]
    '''
    number_of_game = 0
    number_of_first = 0
    number_of_second = 0
    number_of_third = 0
    number_of_fourth = 0
    for game_result in list_game_game_history: #loop over the game result
        if game_result[2] == race_distance: #if the game result is equal to target distance
            number_of_game +=1
            try: #check whether it has result of the game
                place = int(game_result[1])
                if place == 1:
                    number_of_first +=1
                if place == 2:
                    number_of_second +=1
                if place == 3:
                    number_of_third +=1
                if place == 4:
                    number_of_fourth +=1
            except ValueError: #pass it if no result of the game
                pass

    return [number_of_game, number_of_first, number_of_second, number_of_third, number_of_fourth]

def get_class_change(game_history, current_class):
    try:
        current_class = current_class.lower().replace('class','').strip()
        last_game = game_history[0]
        last_class = last_game[-1]
        last_class = last_class.lower().replace('class','').strip()
    except:
        return 'Unknown'
    try:
        current_class = int(current_class)
        last_class = int(last_class)
        if current_class < last_class:
            return '升班'
        if current_class == last_class:
            return '同班'
        if current_class > last_class:
            return '降班'

    except:

        return 'Unknown'

def get_hourse_condition(game_history, match_date_str):
    try:
        last_game_date_str = game_history[0][0]
        last_game_date_str = datetime.strftime(last_game_date_str, '%Y/%m/%d')
        last_game_date = last_game_date_str.split('/')
        last_game_date = date(int(last_game_date[0]), int(last_game_date[1]), int(last_game_date[2]))

        match_date_str = match_date_str.split('/')
        match_date = date(int(match_date_str[0]), int(match_date_str[1]), int(match_date_str[2]))

        delta = match_date - last_game_date

        if delta.days < 45:
            status = '正常'
        else:
            status = '差'
    except:
        return 'Unknown', 'Unknown', 'Unknown'

    return last_game_date_str, delta.days, status

