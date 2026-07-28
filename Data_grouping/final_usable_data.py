import json 
import sys 

with open("fight_group_dict.json", 'r') as f1:
    fights_dict=json.load(f1)
with open("updated_fighter_stats.json",'r') as f2:
    fighter_stats=json.load(f2)

'''fight_temp=fights_dict["https://sports-statistics.com/ufc/ufc-fight-statistics/ufc-328-chimaev-vs-strickland/khamzat-chimaev-v-sean-strickland/"]
round_chips=fight_temp["roundchips"]
if(round_chips["round1chip"]):
    print(str(round_chips["round1chip"]).split(("\u2013")))
'''

error_list=[]
usable_data=[]
for k in fights_dict:
    print(k) #testing
    try:
        fight_info=fights_dict[k]
        info={
            "outcome":None,
            "ss-1":None,
            "ts-1":None,
            "knocks-1":None,
            "tkd-lnd-1":None,
            "tkd-att-1":None,
            "sub-att-1":None,
            "h-tar-1":None,
            "b-tar-1":None,
            "l-tar-1":None,
            "dist-pos-1":None,
            "clinch-pos-1":None,
            "ground-pos-1":None,
            "r1-ts-1":None,
            "r1-ss-1":None,
            "r2-ts-1":None,
            "r2-ss-1":None,
            "r3-ts-1":None,
            "r3-ss-1":None,
            "r4-ts-1":None,
            "r4-ss-1":None,
            "r5-ts-1":None,
            "r5-ss-1":None,
            "r1-td-1":None,
            "r2-td-1":None,
            "r3-td-1":None,
            "r4-td-1":None,
            "r5-td-1":None,
            "r1-kd-1":None,
            "r2-kd-1":None,
            "r3-kd-1":None,
            "r4-kd-1":None,
            "r5-kd-1":None,
            "age-1":None,
            "height-1":None,
            "weight-1":None,
            "reach-1":None,
            "leg_reach-1":None,
            "ranking-1":None,
            "ss-2":None,
            "ts-2":None,
            "knocks-2":None,
            "tkd-lnd-2":None,
            "tkd-att-2":None,
            "sub-att-2":None,
            "h-tar-2":None,
            "b-tar-2":None,
            "l-tar-2":None,
            "dist-pos-2":None,
            "clinch-pos-2":None,
            "ground-pos-2":None,
            "r1-ts-2":None,
            "r1-ss-2":None,
            "r2-ts-2":None,
            "r2-ss-2":None,
            "r3-ts-2":None,
            "r3-ss-2":None,
            "r4-ts-2":None,
            "r4-ss-2":None,
            "r5-ts-2":None,
            "r5-ss-2":None,
            "r1-td-2":None,
            "r2-td-2":None,
            "r3-td-2":None,
            "r4-td-2":None,
            "r5-td-2":None,
            "r1-kd-2":None,
            "r2-kd-2":None,
            "r3-kd-2":None,
            "r4-kd-2":None,
            "r5-kd-2":None,
            "age-2":None,
            "height-2":None,
            "weight-2":None,
            "reach-2":None,
            "leg_reach-2":None,
            "ranking-2":None,
        }
        #Round-wise td/kd values extracted
        roundchips=fight_info["roundchips"]
        for i in range(1,6):
            if(roundchips[f"round{i}chip"]):
                chip=roundchips[f"round{i}chip"].strip()
                chip_key=chip.split()[0]
                chip_vals=chip.split()[1].split("\u2013")
                if(chip_key=="TD"):
                    info[f"r{i}-td-1"]=int(chip_vals[0])
                    info[f'r{i}-td-2']=int(chip_vals[1])
                else:
                    info[f"r{i}-kd-1"]=int(chip_vals[0])
                    info[f"r{i}-kd-2"]=int(chip_vals[1])

        #Gather fighter-1 data
        f1=fight_info["fighter1"]
        f1_id=f1["fighter_id"]

        #Outcome set
        oc=f1["status"].upper()
        if(oc=="LOSS"):
            info["outcome"]=0
        else:
            info["outcome"]=1

        info["ss-1"]=int(f1["sig-str"])
        info["ts-1"]=int(f1["tot-str"])
        info["knocks-1"]=int(f1["knocks"])
        info["tkd-lnd-1"]=int(f1["tkd-lnd"])
        if(int(f1["tkd-lnd"])!=0):
            info["tkd-att-1"]=(int(f1["tkd-lnd"])*100)//int(f1["tkd-acc"].strip("%"))
        info["sub-att-1"]=int(f1["sub-att"])
        info["h-tar-1"]=int(f1["head-targets"])
        info["b-tar-1"]=int(f1["body-target"])
        info["l-tar-1"]=int(f1["leg-target"])
        info["dist-pos-1"]=int(f1["distance-pos"])
        info["clinch-pos-1"]=int(f1["clinch-pos"])
        info["ground-pos-1"]=int(f1["ground-pos"])
        if(f1["r1-tot-str"]):
            info["r1-ts-1"]=int(f1["r1-tot-str"])
        if(f1["r1-sig-str"]):
            info["r1-ss-1"]=int(f1["r1-sig-str"])
        if(f1["r2-tot-str"]):
            info["r2-ts-1"]=int(f1["r2-tot-str"])
        if(f1["r2-sig-str"]):
            info["r2-ss-1"]=int(f1["r2-sig-str"])
        if(f1["r3-tot-str"]):
            info["r3-ts-1"]=int(f1["r3-tot-str"])
        if(f1["r3-sig-str"]):
            info["r3-ss-1"]=int(f1["r3-sig-str"])
        if(f1["r4-tot-str"]):
            info["r4-ts-1"]=int(f1["r4-tot-str"])
        if(f1["r4-sig-str"]):
            info["r4-ss-1"]=int(f1["r4-sig-str"])
        if(f1["r5-tot-str"]):
            info["r5-ts-1"]=int(f1["r5-tot-str"])
        if(f1["r5-sig-str"]):
            info["r5-ss-1"]=int(f1["r5-sig-str"])

        if(f1_id):
            if(fighter_stats[str(f1_id)]):
                if(fighter_stats[str(f1_id)]["age"]):
                    info["age-1"]=int(fighter_stats[str(f1_id)]["age"])
                if(fighter_stats[str(f1_id)]["height"]):
                    info["height-1"]=float(fighter_stats[str(f1_id)]["height"])
                if(fighter_stats[str(f1_id)]["weight"]):
                    info["weight-1"]=float(fighter_stats[str(f1_id)]["weight"])
                if(fighter_stats[str(f1_id)]["reach"]):
                    info["reach-1"]=float(fighter_stats[str(f1_id)]["reach"])
                if(fighter_stats[str(f1_id)]["leg_reach"]):
                    info["leg_reach-1"]=float(fighter_stats[str(f1_id)]["leg_reach"])
                info["ranking-1"]=fighter_stats[str(f1_id)]["ranking"]

        f2=fight_info["fighter2"]
        f2_id=f2["fighter_id"]

        info["ss-2"]=int(f2["sig-str"])
        info["ts-2"]=int(f2["tot-str"])
        info["knocks-2"]=int(f2["knocks"])
        info["tkd-lnd-2"]=int(f2["tkd-lnd"])
        if(int(f1["tkd-lnd"])!=0):
            info["tkd-att-2"]=(int(f2["tkd-lnd"])*100)//int(f1["tkd-acc"].strip("%"))
        info["sub-att-2"]=int(f2["sub-att"])
        info["h-tar-2"]=int(f2["head-target"])
        info["b-tar-2"]=int(f2["body-target"])
        info["l-tar-2"]=int(f2["leg-target"])
        info["dist-pos-2"]=int(f2["distance-pos"])
        info["clinch-pos-2"]=int(f2["clinch-pos"])
        info["ground-pos-2"]=int(f2["ground-pos"])
        if(f2["r1-tot-str"]):
            info["r1-ts-2"]=int(f2["r1-tot-str"])
        if(f2["r1-sig-str"]):
            info["r1-ss-2"]=int(f2["r1-sig-str"])
        if(f2["r2-tot-str"]):
            info["r2-ts-2"]=int(f2["r2-tot-str"])
        if(f2["r2-sig-str"]):
            info["r2-ss-2"]=int(f2["r2-sig-str"])
        if(f2["r3-tot-str"]):
            info["r3-ts-2"]=int(f2["r3-tot-str"])
        if(f2["r4-sig-str"]):
            info["r3-ss-2"]=int(f2["r3-sig-str"])
        if(f2["r4-tot-str"]):
            info["r4-ts-2"]=int(f2["r4-tot-str"])
        if(f2["r4-sig-str"]):
            info["r4-ss-2"]=int(f2["r4-sig-str"])
        if(f2["r5-tot-str"]):
            info["r5-ts-2"]=int(f2["r5-tot-str"])
        if(f2["r5-sig-str"]):
            info["r5-ss-2"]=int(f2["r5-sig-str"])

        if(f2_id):
            if(fighter_stats[str(f2_id)]):
                if(fighter_stats[str(f2_id)]["age"]):
                    info["age-2"]=int(fighter_stats[str(f2_id)]["age"])
                if(fighter_stats[str(f2_id)]["height"]):
                    info["height-2"]=float(fighter_stats[str(f2_id)]["height"])
                if(fighter_stats[str(f2_id)]["weight"]):
                    info["weight-2"]=float(fighter_stats[str(f2_id)]["weight"])
                if(fighter_stats[str(f2_id)]["reach"]):
                    info["reach-2"]=float(fighter_stats[str(f2_id)]["reach"])
                if(fighter_stats[str(f2_id)]["leg_reach"]):
                    info["leg_reach-2"]=float(fighter_stats[str(f2_id)]["leg_reach"])
                info["ranking-2"]=fighter_stats[str(f2_id)]["ranking"]

        print(info)
        usable_data.append(info)

    except Exception as e:
        print(f"{k}-> {e}")
        error_list.append(k)

#print(error_list) #only one fight is in error_list we ignore it. 

with open("usable_data.json",'w') as f3:
    json.dump(usable_data,f3,indent=4)