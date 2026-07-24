import sys
import json 

with open("stats_per_fight.json",'r') as f:
    events=json.load(f)

fight_dict={}
for event in events:
    fights=event["fights"]
    for fight in fights:
        fight_dict[fight["fight_link"]]=fight

with open("fight_group_dict.json",'w') as f1:
    json.dump(fight_dict,f1,indent=4)