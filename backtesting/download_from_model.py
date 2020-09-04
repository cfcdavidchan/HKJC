from helper import helper # imporrt helper function
from pprint import pprint
cred_json = 'HKJC-google-cred.json'
worksheet_key = '1jrD0x3qlBVELqyqMUDrIIHj0h66RYIlx48JELNd8ERQ'

google = helper.google_sheet_manager(cred_json, worksheet_key)
all_sheet = google.all_sheet_name_dict()

get_all_model = google.get_every_row(all_sheet['模型'])

# splitting the game into list
all_games = []
game_result = []
for row in get_all_model[2:]:
    if (row[0] == '日期') and (row[1] == '場次'):
        if len(game_result)>0:
            all_games.append(game_result)
        game_result = []
    else:
        game_result.append(row)

for game in all_games:
    print (game)


import json
# Writing to a file
with open('game_model_stage1.json', 'w') as outfile:
    json.dump(all_games, outfile)