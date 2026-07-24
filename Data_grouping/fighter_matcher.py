#Experimenting to check how many fighters in the two datasets match and what their status is 
import json 
import sys
import unicodedata

'''
def normalize_name(name):
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    #return name.lower().strip()
    return name.strip()
sys.stdout.reconfigure(encoding='utf-8')

with open('fighters.json', 'r', encoding='utf-8') as f:
    pri_fighters_data = json.load(f)

with open('Extra_fighters_stats.json', 'r', encoding='utf-8') as f1:
    sec_fighters_data = json.load(f1)

with open("stats_per_fight.json", 'r') as f2:
    fight_stats=json.load(f2) '''

'''sec_fighter_dict={fighter['name']:fighter['fighter_id'] for fighter in sec_fighters_data}
fighter_status_dict={fighter['fighter_id']:fighter['status'] for fighter in sec_fighters_data}
#print(sec_fighter_tuplist)
pri_fighter_list=[fighter['name'] for fighter in pri_fighters_data]
#print(pri_fighter_list) 
matched_fighters=[]
not_matched_fighters=[]
for fighter in pri_fighter_list:
    if fighter in sec_fighter_dict.keys():
        fighter_index=sec_fighter_dict[fighter]
        matched_fighters.append((fighter, fighter_status_dict[fighter_index]))
    else:
        not_matched_fighters.append(fighter)

print(f'Matched fighters: {len(matched_fighters)} and original_dataset: {len(pri_fighter_list)}')
print(matched_fighters)
print("==================================")
print(not_matched_fighters)
# Conclusion a lot of fighters in fighters.json don't match the latter which is vast and more comprehensive
#Thus we use Extra_fighters_stats.json'''
#Primary key for matching ============================================
'''
visited=[]
dup_fighters=[]
fighter_names=set()
for fighter in sec_fighters_data:
    if fighter['status'] not in visited: 
        visited.append(fighter['status'])
    if fighter['name'] not in fighter_names:
        fighter_names.add(fighter['name'])
    else:
        dup_fighters.append(fighter['name'])
'''
#print(f'Unique statuses: {visited}') #['Not Fighting', 'Active', 'Retired', '#6 PFP', '#15 PFP', '#8 PFP', '#10 PFP', '#13 PFP', '#7 PFP', '#5 PFP', '#2 PFP', '#11 PFP', 'Road to UFC', '#1 PFP', '#14 PFP', '#12 PFP', '#9 PFP', '#4 PFP', '#3 PFP']
#print(f'Number of unique fighters: {len(fighter_names)}')#2535
#print(f'Number of duplicate fighters: {len(dup_fighters)}')#3
#print(f'Duplicate fighters: {dup_fighters}')  # ['Joey Gomez', 'Keiichiro Nakamura', 'Bruno Silva']
'''
pri_fighter={}
for fighter in sec_fighters_data:
    pri_fighter[normalize_name(fighter['name'])]=fighter['fighter_id']

#with open('pri-fighter-link.json','w',encoding='utf-8') as f3:
    #json.dump(pri_fighter,f3,indent=4)

#print(pri_fighter)
event_fighter_link=[]
error_link_list=[]
for event in fight_stats:
    fights=event['fights']
    for fight in fights: 
        try:
            fight_id=fight['fight_link']
            fighter1=fight['fighter1']
            fighter1_name=fighter1['fighter_name']
            fighter2=fight['fighter2']
            fighter2_name=fighter2['fighter_name']
            fighter1_id=pri_fighter[normalize_name(fighter1_name)]
            fighter2_id=pri_fighter[normalize_name(fighter2_name)]
            #fighter1_id = pri_fighter.get(normalize_name(fighter1_name))
            #fighter2_id=pri_fighter.get(normalize_name(fighter2_name))
            fighter_link={
                'fight_id': fight_id,
                'fighter1': fighter1_name,
                'fighter1_id': fighter1_id,
                'fighter2': fighter2_name,
                'fighter2_id': fighter2_id
            }
            event_fighter_link.append(fighter_link)
        except Exception as e:
           # print(f'Error linking fight {fight_id}: {e}')
            error_link_list.append(fight_id)
#print(event_fighter_link)
#print(f'Number of successfully linked fights: {len(event_fighter_link)}')
#print(f'Number of fights with errors: {len(error_link_list)}')
#print(f'Error fight IDs: {error_link_list}') 

#Conclusion: The loss of significant fights are due to 
#1. Fighters with special characters in their names 
#2. Old Fights with Fighters that are not in the latter dataset i.e from UFC.com
#print("Joey Gomez" in pri_fighter) 
#print("Keiichiro Nakamura" in pri_fighter)
#print("Bruno Silva" in pri_fighter)
#print(event_fighter_link)
#with open('event_fighter_link.json', 'w', encoding='utf-8') as f3:
 #   json.dump(event_fighter_link, f3, indent=4)

fighter_stats={}
for fighter in sec_fighters_data:
    fighter_stats[fighter["fighter_id"]]=fighter

#print(fighter_stats)

#with open("Extra_fighters_stats.json",'w') as d:
 #   json.dump(fighter_stats,d,indent=4)
'''
#++++++++++++++++++Checking Elo Rating System+++++++++++++++++++++++++++++++
sys.stdout.reconfigure(encoding="utf-8")
with open("event_fighter_link.json",'r') as f:
    event_fighter_link=json.load(f)
with open("Extra_fighters_stats.json",'r') as f1:
    fighter_stats=json.load(f1) #make it accessible by fighter_id (status: done)
with open("fight_group_dict.json",'r') as f2:
    fight_group=json.load(f2)

broken_links=[]
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
    #print(f"==============={fight_link}================")
    #fight_info=fight_group[fight_link]
    fight_info=fight_group.get(fight_link)
    if(fight_info):
        fighter1_info=fight_info["fighter1"]
        fighter2_info=fight_info["fighter2"]
        #print()
        fighter1_status=status_integer(fighter1_info["status"])
        fighter2_status=status_integer(fighter2_info["status"])

        #print(f"f1_stat {fighter1_info["status"]} {fighter1_status}")
        #print(f"f2_stat {fighter2_info["status"]} {fighter2_status}")
        
        f1_rating=fighter_stats[str(fighter1_id)]["ranking"]
        f2_rating=fighter_stats[str(fighter2_id)]["ranking"]

        p1=probability(fighter1_status,f1_rating,f2_rating)
        p2=probability(fighter2_status,f2_rating,f1_rating)
        #print(p1)
        #print(p2)

        #print(fighter_stats[str(fighter1_id)]["ranking"])
        #print(fighter_stats[str(fighter2_id)]["ranking"])
        #print(updated_rating(p2,100,fighter2_status))
        #print(updated_rating(p1,100,fighter1_status))
        dy=fighter_stats[str(fighter2_id)]["ranking"]+updated_rating(p2,100,fighter2_status)
        dx=fighter_stats[str(fighter1_id)]["ranking"]+updated_rating(p1,100,fighter1_status)

        fighter_stats[str(fighter1_id)]["ranking"]=dx
        fighter_stats[str(fighter2_id)]["ranking"]=dy

        #print(fighter_stats[str(fighter1_id)]["ranking"])
        #print(fighter_stats[str(fighter2_id)]["ranking"])
    else:
        broken_links.append(fight_link)

print(f"===============Missing Links--{len(broken_links)}===================")
print(broken_links)

#Conclusion: only one fight is missing