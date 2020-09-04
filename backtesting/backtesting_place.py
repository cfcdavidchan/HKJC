import json
from helper import helper # imporrt helper function

cred_json = 'HKJC-google-cred.json'
worksheet_key = '1r3RVuk76eyEFgNrP9B02i1d51kjFQGKw4bXzh6SgVi4'
google = helper.google_sheet_manager(cred_json, worksheet_key)

with open('game_model_stage1.json') as data_file:
    games_model = json.load(data_file)
print (games_model)
def kelly_formula_suggestion(win_rate, HKJC_odd, money_on_hand):
    p = win_rate
    b = HKJC_odd -1
    kelly_rate = ((p * ( b +1 )) - 1) / b
    kelly_money = money_on_hand * kelly_rate
    return int(kelly_money)
# 可投注 in 37

def kelly_concept(premium):
    '''
    :param premium:
    :return: the suggested multiple
    '''
    if premium >= 100:
        return 2
    if premium >= 80 and premium < 100:
        return 1.8
    if premium >= 60 and premium < 80:
        return 1.6
    if premium >= 40 and premium < 60:
        return 1.4
    if premium >= 20 and premium < 40:
        return 1.2
    else:
        return 1


premium_100_up = 0
premium_100_up_W = 0
premium_100_up_Place = 0
premium_80_up = 0
premium_80_up_W = 0
premium_80_up_Place = 0
premium_60_up = 0
premium_60_up_W = 0
premium_60_up_Place = 0
premium_40_up = 0
premium_40_up_W = 0
premium_40_up_Place = 0
premium_neg = 0
premium_neg_W= 0
premium_neg_Place = 0

def backtesting(kelly=False, win_place= False, place_only=False, hkjc_odd_ignore=10, hkjc_ignoare_first= False, place_multiplier= 3, account_money= 25000, game_invest_base= 1000):
    #money_list = [account_money]
    number_of_win = 0
    number_of_loss = 0
    number_of_invest = 0
    invest_record = []
    for race in games_model: #loop over each race
        # list to include the horse that may buy
        may_buy = []
        for horse in race: # loop over each horse of the race
            # get the reasonable odd of the horse
            if horse[29] == '': #if no reasonable odd, will skip the race
                continue
            else:
                print (horse[29])
                reasonable_odd = float(horse[29])
            # get the HKJC odd of the horse
            if horse[34] == '':  #if no HKJC odd, will skip the race
                continue
            else:
                hkjc_odd = float(horse[34])
            if hkjc_ignoare_first: #skipping the race if the hkjc odd too high
                if hkjc_odd > hkjc_odd_ignore:
                    continue
            # get the place odd of the horse
            if horse[35] == '':
                place_odd = 0
            else:
                place_odd = float(horse[35])
            # get the premium of the horse
            if horse[36] == '':
                premium = 0
            else:
                premium = float(horse[36].replace('%',''))
            # get the final position of the horse
            if horse[40] == '': # if no final position, will skip the race
                continue
            else:
                final_place = horse[40]
            date = horse[0] #race date
            race = horse[1].lower().replace('race','') #race number
            horse_number = horse[8] #horse number
            # add all the horse into consideration
            may_buy.append([reasonable_odd, hkjc_odd, premium, final_place, date, race, horse_number, place_odd])

        if len(may_buy) > 0: # get some horses to buy
            # buy the lowest reasonable_odd horse (most hot in the model)
            target_horse = (min(may_buy, key=lambda x: x[0]))
            reasonable_odd = float(target_horse[0])
            hkjc_odd = float(target_horse[1])
            premium = float(target_horse[2])
            final_place = target_horse[3]

            date = target_horse[4]
            race = target_horse[5]
            horse_number = target_horse[6]
            place_odd = target_horse[7]

            if account_money <10: #buy hourse only if the account has more than 10 dollars
                print ('Game Over')
                break
            else:
                if hkjc_odd > hkjc_odd_ignore: #if the hkjc_odd is too cold, skip the game
                    continue

                # decide the money to invest
                if kelly: #using kelly concept
                    kelly_multipler =kelly_concept(premium)
                    game_invest = game_invest_base * kelly_multipler
                else:
                    game_invest = game_invest_base

                if win_place: #buy both win and place
                    win_invest = game_invest - game_invest % 10 #make it can be divide by 10
                    place_invest = win_invest * place_multiplier
                else: # buy win only
                    win_invest = game_invest - game_invest % 10 #make it can be divide by 10
                    place_invest = 0
                if place_only:
                    win_invest = 0
                    place_invest = game_invest - game_invest % 10 #make it can be divide by 10

                # initialize the P_L of the game annd record it
                race_P_L = 0
                # P_L from win
                if final_place in [1, '1']:
                    win_P_L = win_invest * (hkjc_odd -1)
                else:
                    win_P_L = 0 - win_invest

                # P_L from place
                if final_place in [1,2,3,'1','2','3']:
                    place_P_L = place_invest * (place_odd - 1)
                else:
                    place_P_L = 0 - place_invest

                race_P_L = win_P_L + place_P_L # P_L of the whole race

                total_invest = win_invest + place_invest
                orginial_account_money = account_money
                account_money = account_money + race_P_L # P_L contribution to the account money

                record = [date, race, horse_number, win_invest, hkjc_odd, win_P_L, place_invest, place_odd, place_P_L, total_invest, race_P_L, orginial_account_money, account_money]
                #money_list.append(account_money)
                invest_record.append(record)
                number_of_invest += 1
                if race_P_L >0:
                    number_of_win += 1
                elif race_P_L <0:
                    number_of_loss += 1

    return account_money, invest_record, number_of_win, number_of_loss, number_of_invest

# optimization
result_ignore_first = {}
for i in range(1, 21):
    kelly = True
    win_place = True
    place_only = False
    place_multiplier = i
    account_money = 25000
    game_invest_base = 1000
    hkjc_odd_ignore = 15
    hkjc_ignoare_first = True

    account_money, invest_record, number_of_win, number_of_loss, number_of_invest = backtesting(kelly=kelly, win_place= win_place, place_only=place_only, hkjc_odd_ignore=hkjc_odd_ignore, hkjc_ignoare_first=hkjc_ignoare_first, place_multiplier= place_multiplier, account_money= account_money, game_invest_base= game_invest_base)
    try:
        win_rate = number_of_win/number_of_invest
    except:
        win_rate = 0
    result_ignore_first[i] = [account_money, win_rate]

result_ignore_later = {}
for i in range(1, 21):
    kelly = True
    win_place = True
    place_only = False
    place_multiplier = i
    account_money = 25000
    game_invest_base = 1000
    hkjc_odd_ignore = 15
    hkjc_ignoare_first = False

    account_money, invest_record, number_of_win, number_of_loss, number_of_invest = backtesting(kelly=kelly, win_place= win_place, place_only=place_only, hkjc_odd_ignore=hkjc_odd_ignore, hkjc_ignoare_first=hkjc_ignoare_first, place_multiplier= place_multiplier, account_money= account_money, game_invest_base= game_invest_base)
    try:
        win_rate = number_of_win/number_of_invest
    except:
        win_rate = 0
    result_ignore_later[i] = [account_money, win_rate]


from pprint import pprint
print ('Ignore First')
pprint (result_ignore_first)
print ('Ignore Later')
pprint (result_ignore_later)

# kelly = True
# win_place = True
# place_only = False
# place_multiplier = 3
# account_money = 25000
# game_invest_base = 1000
# hkjc_odd_ignore = 15
# hkjc_ignoare_first = True
# account_money, invest_record, number_of_win, number_of_loss, number_of_invest = backtesting(kelly=kelly, win_place= win_place, place_only=place_only, hkjc_odd_ignore=hkjc_odd_ignore, hkjc_ignoare_first=hkjc_ignoare_first, place_multiplier= place_multiplier, account_money= account_money, game_invest_base= game_invest_base)
# print (account_money)
# print ('Win Rate: ', number_of_win/number_of_invest)
#
# # # store it to google
# sheet_name = '1W_3P_15_kelly_ignore_first_stage_1'
# #
# # final edit to the data
# header = ['Date', 'Race', 'Horse Number', 'Win Invest', 'Win odd ', 'Win P/L', 'Place Invest', 'Place odd', 'Place P/L', 'Total Invest', 'Total P/L', 'Orginal Money', 'Updated Account']
# invest_record.insert(0, header)
# invest_record[1].extend(['','Final P/L'])
# invest_record[2].extend(['',account_money])
# invest_record[4].extend(['','Number of Win:'])
# invest_record[5].extend(['',number_of_win])
# invest_record[7].extend(['','Number of Loss:'])
# invest_record[8].extend(['',number_of_loss])
# invest_record[10].extend(['','Positive Profit Rate'])
# invest_record[11].extend(['',number_of_win/number_of_invest])
# ##
#
# google.create_spreadsheet(sheet_name=sheet_name,cols=15, rows=300)
# all_sheet = google.all_sheet_name_dict()
# get_all_model = google.clean_and_write(all_sheet[sheet_name], invest_record)
