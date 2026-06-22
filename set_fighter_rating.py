import json 
import sys 
import unicodedata
sys.stdout.reconfigure(encoding='utf-8')
with open("Extra_fighters_stats.json",'r',encoding='utf-8') as f1:
    fighter_stats=json.load(f1)
with open('pri-fighter-link.json','r',encoding='utf-8') as f2:
    pri_fighter_link=json.load(f2)

def normalize_name(name):
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    #return name.lower().strip()
    return name.strip()

for fighter in fighter_stats:
    fighter["ranking"]=1500
    #fighter["fid"]=pri_fighter_link[normalize_name(fighter['name'])]
    #print(fighter)
print(fighter_stats)
with open("Extra_fighters_stats.json",'w') as f2:
    json.dump(fighter_stats,f2,indent=4)