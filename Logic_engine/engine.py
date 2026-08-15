import json 
import sys 
import joblib #type: ignore
import requests
import sklearn #type:ignore
from sklearn.linear_model import LogisticRegression #type:ignore

with open("pri-fighter-link.json",'r') as f:
    pkf=json.load(f)
with open("fighter_fights_group.json",'r') as f2:
    fight_links=json.load(f2)
with open("fight_group_dict.json",'r') as f3:
    group1=json.load(f3) #will give fighter form 
with open("updated_fighter_stats.json",'r') as f4:
    group2=json.load(f4) #static stats
pipe_=joblib.load("lrqt.joblib")
pipe1=joblib.load("rfc.joblib")

def get_static_stats(k):
    stats=group2[str(k)]
    age=stats["age"]
    height=stats["height"]
    weight=stats["weight"]
    reach=stats["reach"]
    leg_reach=stats["leg_reach"]
    ranking=stats["ranking"]

    return [age, height, weight, reach, leg_reach,ranking]

def get_average_form(k):
    links=fight_links[str(k)][1:]
    ss=[]
    ts=[]
    knocks=[]
    tkd_lnd=[]
    tkd_att=[]
    sub_att=[]
    h_tar=[]
    b_tar=[]
    l_tar=[]
    dist_pos=[]
    clinch_pos=[]
    ground_pos=[]
    for i in range(min(5,len(links))):
        fight=links[i]
        stats=group1[fight]
        f1=stats["fighter1"]
        f2=stats["fighter2"]
        if(k==f1["fighter_id"]):
            ss.append(int(f1["sig-str"]))
            ts.append(int(f1["tot-str"]))
            knocks.append(int(f1["knocks"]))
            tkd_lnd.append(int(f1["tkd-lnd"]))
            if(int(f1["tkd-acc"].strip().split("%")[0])!=0):
                 tkd_att.append(int(f1["tkd-lnd"])//(int(f1["tkd-acc"].strip().split("%")[0])/100))                   
            else:
                tkd_att.append(int(f1["tkd-lnd"]))
            sub_att.append(int(f1["sub-att"]))
            h_tar.append(int(f1["head-targets"]))
            b_tar.append(int(f1["body-target"]))
            l_tar.append(int(f1["leg-target"]))
            dist_pos.append(int(f1["distance-pos"]))
            clinch_pos.append(int(f1["clinch-pos"]))
            ground_pos.append(int(f1["ground-pos"]))
        if(k==f2["fighter_id"]):
            ss.append(int(f2["sig-str"]))
            ts.append(int(f2["tot-str"]))
            knocks.append(int(f2["knocks"]))
            tkd_lnd.append(int(f2["tkd-lnd"]))
            if(int(f2["tkd-acc"].strip().split("%")[0])!=0):
                tkd_att.append(int(f2["tkd-lnd"])//(int(f2["tkd-acc"].strip().split("%")[0])/100))                   
            else:
                tkd_att.append(int(f2["tkd-lnd"]))
            sub_att.append(int(f1["sub-att"]))
            h_tar.append(int(f2["head-target"]))
            b_tar.append(int(f2["body-target"]))
            l_tar.append(int(f2["leg-target"]))
            dist_pos.append(int(f2["distance-pos"]))
            clinch_pos.append(int(f2["clinch-pos"]))
            ground_pos.append(int(f2["ground-pos"]))
    dynamic_features=[]
    dynamic_features.append((sum(ss))//len(ss))
    dynamic_features.append((sum(ts))//len(ts))
    dynamic_features.append((sum(knocks))//len(knocks))
    dynamic_features.append((sum(tkd_lnd))//len(tkd_lnd))
    dynamic_features.append(sum(tkd_att)//len(tkd_att))
    dynamic_features.append(sum(sub_att)//len(sub_att))
    dynamic_features.append(sum(h_tar)//len(h_tar))
    dynamic_features.append(sum(b_tar)//len(b_tar))
    dynamic_features.append(sum(l_tar)//len(l_tar))
    dynamic_features.append(sum(dist_pos)//len(dist_pos))
    dynamic_features.append(sum(clinch_pos)//len(clinch_pos))
    dynamic_features.append(sum(ground_pos)//len(ground_pos))
    return dynamic_features



def get_feature(k):
    fly1=get_static_stats(k)
    fly2=get_average_form(k)
    feature=fly2.copy()
    for i in range(len(fly1)):
        feature.append(fly1[i])
    return feature

def build_features(name1,name2):
    names=list(pkf.keys())
    try:
        k1=pkf[name1]
        k2=pkf[name2]
        feature1=get_feature(k1)
        feature2=get_feature(k2)
        features=feature1.copy()
        for i in range(len(feature2)):
            features.append(feature2[i])
        return features
        
    except requests.exceptions.Timeout as e:
        print("Fighter Unavailable!")
        print(type(e).__name__)
        failed=[]
        return failed

def fighter_prob(name1, name2):
    features=build_features(name1,name2)
    #features=pipe_.transform(features)
    probs=pipe_.predict_proba([features])
    #print(pipe_.predict_proba([features]))

    #print("++++++++++RESULTS++++++++++")
    f1_prob=float(f"{probs[0][1]*100:.2f}%")
    f2_prob=float(f"{probs[0][0]*100:.2f}%")

    x=pipe1.predict([features])
    if(x==1):
        winner=name1
        winner_prob=f1_prob
    else:
        winner=name2
        winner_prob=f2_prob
    return winner,winner_prob



#NOTE: 0 means fighter 2 wins, 1 means fighter 1 wins