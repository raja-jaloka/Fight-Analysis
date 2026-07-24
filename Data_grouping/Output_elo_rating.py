import sys 
import json 
sys.stdout.reconfigure(encoding="utf-8")

with open("updated_fighter_stats.json",'r') as f:
    stats_dict=json.load(f)

values_list=stats_dict.values()

values_list=sorted(values_list,reverse=True,key= lambda x: x["ranking"])

for val in values_list:
    print(f"{val["name"]} {val["ranking"]}")