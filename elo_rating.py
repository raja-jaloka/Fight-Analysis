import json
import sys 
sys.stdout.reconfigure(encoding="utf-8")
with open("event_fighter_link.json",'r') as f:
    event_fighter_link=json.load(f)
with open("Extra_fighters_stats.json",'r') as f1:
    fighter_stats=json.load(f1) #make it accessible by fighter_id (status: done)
with open("fight_group_dict.json",'r') as f2:
    fight_group=json.load(f2)

def status_integer(s):
    if(s=="LOSS"):
        return 0
    elif(s=="WIN"):
        return 1
    else:
        return 0.5

def probability(status,r1,r2):
    diff=r1-r2
    diff=diff/400
    denom=1+(10**(diff))
    return 1/denom

def updated_rating(p,k,status):
    return k*(status-p)

for event in reversed(event_fighter_link):
    fight_link=event["fight_id"]
    #print(type(fight_link))
    fighter1_id=event["fighter1_id"]
    fighter2_id=event["fighter2_id"]
    print(f"==============={fight_link}================")
    #fight_info=fight_group[fight_link]
    fight_info=fight_group.get(fight_link)
    if(fight_info):
        fighter1_info=fight_info["fighter1"]
        fighter2_info=fight_info["fighter2"]
        print()
        fighter1_status=status_integer(fighter1_info["status"])
        fighter2_status=status_integer(fighter2_info["status"])

        print(f"f1_stat {fighter1_info["status"]} {fighter1_status}")
        print(f"f2_stat {fighter2_info["status"]} {fighter2_status}")
        
        f1_rating=fighter_stats[str(fighter1_id)]["ranking"]
        f2_rating=fighter_stats[str(fighter2_id)]["ranking"]

        p1=probability(fighter1_status,f1_rating,f2_rating)
        p2=probability(fighter2_status,f2_rating,f1_rating)
        print(p1)
        print(p2)

        print(fighter_stats[str(fighter1_id)]["ranking"])
        print(fighter_stats[str(fighter2_id)]["ranking"])
        print(updated_rating(p2,40,fighter2_status))
        print(updated_rating(p1,40,fighter1_status))
        dy=fighter_stats[str(fighter2_id)]["ranking"]+updated_rating(p2,100,fighter2_status)
        dx=fighter_stats[str(fighter1_id)]["ranking"]+updated_rating(p1,100,fighter1_status)

        fighter_stats[str(fighter1_id)]["ranking"]=dx
        fighter_stats[str(fighter2_id)]["ranking"]=dy

        print(fighter_stats[str(fighter1_id)]["ranking"])
        print(fighter_stats[str(fighter2_id)]["ranking"])

        

print(fighter_stats)
with open("updated_fighter_stats.json",'w') as f3:
    json.dump(fighter_stats,f3,indent=4) 
#Problem1 (Status:Solved): ranking per iteration is not updated leading to a constant 0.5 probability due to unupdated initial ranking i.e 1500