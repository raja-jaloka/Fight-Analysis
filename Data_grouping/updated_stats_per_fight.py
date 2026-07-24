import sys 
import json 

with open("fight_group_dict.json",'r') as f:
    events=json.load(f)

with open("pri-fighter-link.json",'r') as f1:
    pri_fighter_link=json.load(f1)

for event in events:
    fight_night=events[event]
    

    fighter1=fight_night["fighter1"]
    fighter1_name=fighter1["fighter_name"]
    if(fighter1_name in pri_fighter_link):
        fighter1_id=pri_fighter_link[fighter1_name]
    else:
        fighter1_id=None

    fighter2=fight_night["fighter2"]
    fighter2_name=fighter2["fighter_name"]
    if(fighter2_name in pri_fighter_link):
            fighter2_id=pri_fighter_link[fighter2_name]
    else:
        fighter2_id=None

    

    fighter1["fighter_id"]=fighter1_id
    fighter2["fighter_id"]=fighter2_id

print(events)

with open("fight_group_dict.json",'w') as f2:
    json.dump(events,f2,indent=4)