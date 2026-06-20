import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('event_fighter_link.json','r') as f:
    events=json.load(f)

def fight_append(f1,f1id,flink):
    if(f1id in fighter_fights):
        fighter_fights[f1id].append(flink)
    else:
        fighter_fights[f1id]=[f1,flink]

fighter_fights={}
for event in events:
    fight_append(event["fighter1"],event["fighter1_id"],event["fight_id"])
    fight_append(event["fighter2"],event["fighter2_id"],event["fight_id"])

#print(fighter_fights)
print(len(fighter_fights))
with open("fighter_fights_group.json",'w') as f1:
    json.dump(fighter_fights,f1,indent=4)