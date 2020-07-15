from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%H:%M:%S")

odds = [dt_string,{'1':[2],
                   '2':[1],
                   '3':[10]}]

import json

filename = 'odds.json'
# function to add to JSON
def write_json(data, filename= filename):
    with open(filename,'w') as f:
        json.dump(data, f, indent=4)

with open(filename) as json_file:
    data = json.load(json_file)
    data.append(odds)

write_json(data)