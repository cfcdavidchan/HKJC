import sys, os
from datetime import date, datetime

base_path = os.path.realpath(__file__)
base_path = os.path.dirname(base_path)
global chrome_path
chrome_path = os.path.join(base_path, 'chromedriver')

def get_chrome_path():
    return chrome_path

##Obtain django data

base_path = sys.path[0] # obtain the path of this directory
project_path = os.path.abspath(os.path.join(base_path, '../../'))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','HKJC.settings')
import django
django.setup()

from HKJC_database.models import Jockey_Info, Trainer_Info, Horse_Info, Match_Result, Match_Info
from django.forms.models import model_to_dict

def get_horse_chi_name(horse_english_name):
    try:
        horse = Horse_Info.objects.get(name=horse_english_name)
        return horse.chinese_name
    except Horse_Info.DoesNotExist:
        return None

def get_horse_age(horse_english_name):
    try:
        horse = Horse_Info.objects.get(name=horse_english_name)
        return horse.age
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
    :return:  [[match_date, place, distance of game, game_place, class of the game, game_course]]
    '''
    game_history = []
    try:
        horse = Horse_Info.objects.get(name=horse_name)

        match_result = Match_Result.objects.filter(horse=horse)
        for result in match_result: #loop over all tge game
            match_date = result.match.match_date
            place = result.horse_place
            race_distance = result.match.distance_M
            game_class = result.match.match_class
            game_place = result.match.match_place
            game_course = result.match.match_course
            game_data = [match_date, place, race_distance, game_place, game_class, game_course]

            game_history.append(game_data)
    except:
        pass

    def sort_date(elem):
        return elem[0]
    game_history.sort(key=sort_date, reverse=True) # sort the result by date
    return game_history


def get_result_by_distance(list_game_game_history, race_distance, match_place, race_course):
    '''
    :param list_game_game_history: [[match_date, place, distance of game], ...]
    :return: [number of game, number of No.1, number of No.2, number of No.3, number of No.4]
    '''

    def distance_range(match_place, race_distance, race_course):
        '''
        :param match_place: sha tin or happy valley
        :param race_distance: int()
        :param track:  turf or all weather
        :return: list()
        '''
        distance_range_dict = {'happy valley':
                                   {'turf':
                                        {'short_range': [1000, 1200],
                                         'mid_range': [1650, 1800],
                                         'long_range': [1800, 2000, 2200, 2400]
                                         }
                                    },
                               'sha tin':
                                   {'turf':
                                        {'short_range': [1000],
                                         'mid_range': [1200, 1400, 1600],
                                         'long_range': [1800, 2000, 2200, 2400]
                                         },
                                    'all weather track':
                                        {'short_range': [1200],
                                         'mid_range': [1650, 1800],
                                         'long_range': [2000, 2400]
                                         }
                                    }
                               }

        for race_range, distance_list in distance_range_dict[match_place.lower()][race_course.lower()].items():
            if race_distance in distance_list:
                #print(race_range)
                return distance_list

    distance_list = distance_range(match_place, race_distance, race_course)
    #print (list_game_game_history)
    number_of_game = 0
    number_of_first = 0
    number_of_second = 0
    number_of_third = 0
    number_of_fourth = 0

    for game_result in list_game_game_history: #loop over the game result
        if (game_result[2] in distance_list) and (game_result[3] == match_place) and (race_course.lower() in game_result[5]): #if the game result is equal to target distance
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
    game_class_history = []
    class_change = ''

    if len(game_history) == 0: # no game history
        class_change = 'unknown'
        return game_class_history, class_change
    else:
        game_class_history = [game[4] for game in game_history]

    if len(game_class_history) > 3:
        game_class_history = game_class_history[:3]

    try:
        current_class = int(current_class.lower().replace('class', '').strip())
    except: #cannot compare
        class_change = 'unknown'
        return game_class_history, class_change

    compare_class_history = []
    for i in range(3):
        try:
            game_class = int(game_class_history[i].lower().replace('class','').strip())
        except:
            game_class = None
        compare_class_history.append(game_class)

    while None in compare_class_history:
        compare_class_history.remove(None)

    if len(compare_class_history) == 0:
        class_change = 'unknown'
        return game_class_history, class_change
    # 1 > 2 > 3 > 4 > 5
    highest_class = min(compare_class_history)
    lower_class = max(compare_class_history)

    class_change = 'unknown'
    if  current_class > highest_class:
        class_change = '降班'
    if  current_class < lower_class:
        class_change = '升班'
    if (current_class == lower_class) and (current_class == highest_class):
        class_change = '同班'

    return game_class_history, class_change

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
        elif delta.days < 180:
            status = '差'
        else:
            status = '極差'
    except:
        return 'Unknown', 'Unknown', 'Unknown'

    return last_game_date_str, delta.days, status

def get_recent_time_record(horse_name="", reference_year= 3, match_place="", distance=0, race_course=""):
    # test input
    # match_place = "happy valley"
    # horse_name = "MAGNETISM"
    # distance = 2200
    #get horse id
    def record_to_seconds(record):
        mins, seconds = record.split(":")
        return int(mins) * 60 + float(seconds)
    try:
        horse_id = Horse_Info.objects.get(name=horse_name).id
        #current year
        current_year = datetime.now().year
        #all reference year
        reference_year = [current_year - i for i in range(0,reference_year)]
        #all related match
        all_match_id = []
        for year in reference_year:
            year_match_id = Match_Info.objects.filter(match_date__contains= year,
                                                      match_course__contains= race_course,
                                                      match_place=match_place,
                                                      distance_M = distance).values_list('id', flat=True)
            if len(year_match_id) > 0:
                for match_id in year_match_id:
                    all_match_id.append(match_id)



        all_record_time = []
        #
        for match_id in all_match_id:
            try:
                match_time_string = Match_Result.objects.get(horse_id= horse_id, match_id= match_id).finish_time
                time = record_to_seconds(match_time_string)
                all_record_time.append(time)
            except Match_Result.DoesNotExist:
                pass

        if len(all_record_time) == 0:
            return 0.0

        else:
            all_record_time = sorted(all_record_time)
            # return average time
            return sum(all_record_time)/len(all_record_time)
    except:
        return 0.0

print (get_recent_time_record())