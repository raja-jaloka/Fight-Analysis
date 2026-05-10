import json
import requests
from bs4 import BeautifulSoup

#Part 2: Scrape the detailed fighter data from each fighter's page on UFCstats
fighter_stats=[]

with open('fighters.json', 'r') as f:
    fighters_url=json.load(f)
#print(fighters_url) 

for fighter in fighters_url:
    fighter_id=fighter['fighter_id']
    fighter_url=fighter['fighter_url']
    name=fighter['name']
    height=fighter['height']
    weight=fighter['weight']
    reach=fighter['reach']
    stance=fighter['stance']
    wins=fighter['wins']
    losses=fighter['losses']
    draws=fighter['draws']
    
    page=requests.get(fighter_url)
    if(page.status_code!=200):
        print(f'{page.status_code} Error fetching page data for {fighter_id}')
        exit()
    soup=BeautifulSoup(page.text, 'html.parser')
    rows=soup.find_all('ul', class_="b-list__box-list b-list__box-list_margin-top")
    #if(len(rows)<2):
     #   continue
    leftrow=rows[0]
    rightrow=rows[1]
    leftrow_cols=leftrow.find_all('li', class_="b-list__box-list-item b-list__box-list-item_type_block")
    rightrow_cols=rightrow.find_all('li', class_="b-list__box-list-item b-list__box-list-item_type_block")
    
    #if(len(leftrow_cols)<4 or len(rightrow_cols)<6):
     #   continue

    slpm=leftrow_cols[0].text.strip()
    st_acc=leftrow_cols[1].text.strip()
    sapm=leftrow_cols[2].text.strip()
    st_def=leftrow_cols[3].text.strip()
    TD_avg=rightrow_cols[1].text.strip()
    TD_acc=rightrow_cols[2].text.strip()
    TD_Def=rightrow_cols[3].text.strip()
    Sub_avg=rightrow_cols[4].text.strip()

    stat={
        "fighter_id":fighter_id,
        "fighter_url":fighter_url,
        "name":name,
        "height":height,
        "weight":weight,
        "reach":reach,
        "stance":stance,
        "wins":wins,
        "losses":losses,
        "draws":draws,
        "SLPM": slpm.split(":")[1].strip(),
        "St_acc":st_acc.split(":")[1].strip(),
        "SAPM":sapm.split(":")[1].strip(),
        "St_def":st_def.split(":")[1].strip(),
        "TD_AVG":TD_avg.split(":")[1].strip(),
        "TD_ACC":TD_acc.split(":")[1].strip(),
        "TD_def":TD_Def.split(":")[1].strip(),
        "SUB_AVG":Sub_avg.split(":")[1].strip()
    }
    fighter_stats.append(stat)
    print(stat)

print(fighter_stats)

with open('fighter_stats.json','w') as f:
    json.dump(fighter_stats,f,indent=4)
