import os, sys

base_path = sys.path[0] # obtain the path of this directory
project_path = os.path.abspath(os.path.join(base_path, '../'))
sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE','HKJC.settings')
import django
django.setup()

from HKJC_database.models import Going

track = {'turf':[['Firm', '快地', 'F'],
                 ['Good To Firm', '好至快地', 'G/F'],
                 ['Good', '好地', 'G'],
                 ['Good To Yielding', '好至黏地', 'G/Y'],
                 ['Yielding', '黏地', 'Y'],
                 ['Yielding To Soft', '黏至軟地', 'Y/S'],
                 ['Soft', '軟地', 'S'],
                 ['Heavy', '大爛地', 'H']
                 ],
         'all weather':[['Wet fast', '濕快地', 'WF'],
                        ['Good', '好地', 'GD'],
                        ['Wet slow', '濕慢地', 'WS'],
                        ['Normal watering ', '例常灑水', 'NW'],
                        ['Fast', '快地', 'FT'],
                        ['Slow', '慢地', 'SL'],
                        ['Rain affected', '受天雨影響', 'RA'],
                        ]
         }
for key, value in track.items():
    track = key
    for info in value:
        going_data = Going()
        condition = info[0].lower()
        chinese_condition = info[1]
        code = info[2]

        obj, created = Going.objects.get_or_create(
            track= track,
            condition= condition,
            chinese_condition= chinese_condition,
            code= code
        )
        msg = "track: {}\ncondition: {}\nchinese_condition: {}\ncode: {}".format(track, condition, chinese_condition, code)

        if created:
            print(msg)
            print('Is Successfully added into database')
        else:
            print (msg)
            print ('Is already in the database')
