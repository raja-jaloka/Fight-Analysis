import json 
import sys 
sys.stdout.reconfigure(encoding='utf-8')
with open("Extra_fighters_stats.json",'r',encoding='utf-8') as f1:
    fighter_stats=json.load(f1)

for fighter in fighter_stats:
    fighter["ranking"]=1500
    #print(fighter)
print(fighter_stats)
with open("Extra_fighters_stats.json",'w') as f2:
    json.dump(fighter_stats,f2,indent=4)