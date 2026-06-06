import json
import requests
from bs4 import BeautifulSoup
import sys

eventS=[]
with open('fights_per_event.json') as f:
    events=json.load(f)

events=events[:701] #reduce the data so that very old fights get rejected. 

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36"
}

for event in events:
    event_id=event['event_id'] #attr
    event_title=event['event_title'] #attr
    fights=event['fight']
    for fight in fights:
        fight_link=fight['fight_link']
        page=requests.get(fight_link, headers=headers)
        soup=BeautifulSoup(page.text, 'html.parser')

        #sections to be scraped for each fight 
        fight_card=soup.find('section', class_="ufc-fight-hero")
        h2h=soup.find('section', class_="ufc-h2h")
        target=soup.find('section', class_="ufc-target")
        position=soup.find('section', class_="ufc-position")
        rounds=soup.find('section', class_="ufc-rounds")
        
        if fight_card:
            grid=fight_card.find("div", class_="ufc-vs-grid")
            if(grid):
                divs=grid.find_all("div")
                #fwinner=grid.find("div", class_="ufc-vs-fighter ufc-vs-fighter--win")
                #floser=grid.find("div", class_="ufc-vs-fighter ufc-vs-fighter--loss")
                #middle_strip=grid.find("div", class_="ufc-vs-middle")
                fit1=divs[0]
                middle_strip=divs[1]
                fit2=divs[2]
                if(fit1):
                    f1=fit1.find("h2",class_="ufc-vs-name") #attr
                    status1=fit1.find("p", class_="ufc-vs-result") #attr
                else:
                    f1=None
                    status1=None
                if(fit2):
                    f2=fit2.find("h2",class_="ufc-vs-name") #attr
                    status2=fit2.find("p", class_="ufc-vs-result") #attr
                else:
                    f2=None
                    status2=None
                if(middle_strip):
                    fight_title=middle_strip.find("span", class_="ufc-vs-weight")#attr
                    if(fight_title):
                        fight_title=fight_title.text.strip()
                    else:
                        fight_title=None
                    win_method=middle_strip.find("span", class_="ufc-vs-method-full")#attr
                    if(win_method):
                        win_method=win_method.text.strip()
                    else:
                        win_method=None
                    win_time=middle_strip.find("span", class_="ufc-vs-time")#attr
                    if(win_time):
                        win_time=win_time.text.strip()
                    else:
                        win_time=None
                else:
                    f1=None
                    f2=None
                    fight_title=None
                    win_method=None
                    win_time=None
                    status1=None
                    status2=None
        else:
            f1=None
            f2=None
            fight_title=None
            win_method=None
            win_time=None
            status1=None
            status2=None
        
        if(h2h):
            h2h_rows=h2h.find_all("div", class_="ufc-h2h__row")

            #h2h spans
            sig_str_row=h2h[0].find("span")
            sig_str_acc_row=h2h[1].find("span")
            tot_str_row=h2h[2].find("span")
            knocks_row=h2h[3].find("span")
            tkd_lnd_row=h2h[4].find("span")
            tkd_acc_row=h2h[5].find("span")
            sub_att_row=h2h[6].find("span")
            
            if(sig_str_row):
                f1_sig_str_landed=sig_str_row[0].text.strip() #attr
                f2_sig_str_landed=sig_str_row[2].text.strip() #attr
            else:
                f1_sig_str_landed=None #attr
                f2_sig_str_landed=None #attr

            if(sig_str_acc_row):
                f1_sig_str_acc=sig_str_acc_row[0].text.strip() #attr
                f2_sig_str_acc=sig_str_acc_row[2].text.strip() #attr
            else:
                f1_sig_str_acc=None
                f2_sig_str_acc=None
            if(tot_str_row):
                f1_tot_str=tot_str_row[0].text.strip() #attr
                f2_tot_str=tot_str_row[2].text.strip() #attr
            else:
                f2_tot_str=None
                f1_tot_str=None
            if(knocks_row):
                f1_knocks=knocks_row[0].text.strip() #attr
                f2_knocks=knocks_row[2].text.strip() #attr
            else:
                f1_knocks=None
                f2_knocks=None
            if(tkd_lnd_row):
                f1_tkd_lnd=tkd_lnd_row[0].text.strip() #attr
                f2_tkd_lnd=tkd_lnd_row[2].text.strip() #attr
            else:
                f1_tkd_lnd=None
                f2_tkd_lnd=None
            if(tkd_acc_row):
                f1_tkd_acc=tkd_acc_row[0].text.strip() #attr
                f2_tkd_acc=tkd_acc_row[2].text.strip() #attr
            else:
                f1_tkd_acc=None
                f2_tkd_acc=None
            if(sub_att_row):
                f1_sub_att=sub_att_row[0].text.strip() #attr
                f2_sub_att=sub_att_row[2].text.strip() #attr
            else:
                f1_sub_att=None
                f2_sub_att=None
        
        if(target):
            grid=target.find("div", class_="ufc-target__grid")
            if(grid):
                target_cards=grid.find_all("div", class_="ufc-target__card")
                head_card=target_cards[0].find_all("span")
                body_card=target_cards[1].find_all("span")
                leg_card=target_cards[2].find_all("span")
                if(head_card):
                    f1_head_target=head_card[0].text.strip() #attr
                    f1_head_target_pct=head_card[1].text.strip() #attr
                    f2_head_target=head_card[2].text.strip() #attr
                    f2_head_target_pct=head_card[3].text.strip() #attr
                else:
                    f1_head_target=None
                    f1_head_target_pct=None
                    f2_head_target=None
                    f2_head_target_pct=None
                if(body_card):
                    f1_body_target=body_card[0].text.strip() #attr
                    f1_body_target_pct=body_card[1].text.strip() #attr
                    f2_body_target=body_card[2].text.strip() #attr
                    f2_body_target_pct=body_card[3].text.strip() #attr
                else:
                    f1_body_target=None
                    f1_body_target_pct=None
                    f2_body_target=None
                    f2_body_target_pct=None
                if(leg_card):
                    f1_leg_target=leg_card[0].text.strip() #attr
                    f1_leg_target_pct=leg_card[1].text.strip() #attr
                    f2_leg_target=leg_card[2].text.strip() #attr
                    f2_leg_target_pct=leg_card[3].text.strip() #attr
                else:
                    f1_leg_target=None
                    f1_leg_target_pct=None
                    f2_leg_target=None
                    f2_leg_target_pct=None
            else:
                f1_head_target=None
                f1_head_target_pct=None
                f2_head_target=None
                f2_head_target_pct=None
                f1_body_target=None
                f1_body_target_pct=None
                f2_body_target=None
                f2_body_target_pct=None
                f1_leg_target=None
                f1_leg_target_pct=None
                f2_leg_target=None
                f2_leg_target_pct=None

        if(position):
            grid=position.find("div", class_="ufc-target__grid")
            target_cards=grid.find_all("div", class_="ufc-target__card")
            distance_card=target_cards[0].find_all("span")
            clinch_card=target_cards[1].find_all("span")
            ground_card=target_cards[2].find_all("span")
            if(distance_card):
                f1_distance_pos=distance_card[0].text.strip() #attr
                f1_distance_pos_pct=distance_card[1].text.strip() #attr
                f2_distance_pos=distance_card[2].text.strip() #attr
                f2_distance_pos_pct=distance_card[3].text.strip() #attr
            else:
                f1_distance_pos=None
                f1_distance_pos_pct=None
                f2_distance_pos=None
                f2_distance_pos_pct=None
            if(clinch_card):
                f1_clinch_pos=clinch_card[0].text.strip() #attr
                f1_clinch_pos_pct=clinch_card[1].text.strip() #attr
                f2_clinch_pos=clinch_card[2].text.strip() #attr
                f2_clinch_pos_pct=clinch_card[3].text.strip() #attr
            else:
                f1_clinch_pos=None
                f1_clinch_pos_pct=None
                f2_clinch_pos=None
                f2_clinch_pos_pct=None
            if(body_card):
                f1_ground_pos=ground_card[0].text.strip() #attr
                f1_ground_pos_pct=ground_card[1].text.strip() #attr
                f2_ground_pos=ground_card[2].text.strip() #attr
                f2_ground_pos_pct=ground_card[3].text.strip() #attr
            else:
                f1_ground_pos=None
                f1_ground_pos_pct=None
                f2_ground_pos=None
                f2_ground_pos_pct=None
        else:
            f1_distance_pos=None
            f1_distance_pos_pct=None
            f2_distance_pos=None
            f2_distance_pos_pct=None
            f1_clinch_pos=None
            f1_clinch_pos_pct=None
            f2_clinch_pos=None
            f2_clinch_pos_pct=None
            f1_ground_pos=None
            f1_ground_pos_pct=None
            f2_ground_pos=None
            f2_ground_pos_pct=None
        
        if(rounds):
            round_cards=rounds.find_all("div", class_="ufc-round")
            round1str=round_cards[0].find_all("span", class_="ufc-round__num")
            round2str=round_cards[1].find_all("span", class_="ufc-round__num")
            round3str=round_cards[2].find_all("span", class_="ufc-round__num")
            round4str=round_cards[3].find_all("span", class_="ufc-round__num")
            round5str=round_cards[4].find_all("span", class_="ufc-round__num")

            #round1
            if(round1str):
                f1r1str=round1str[0].text.strip()
                f1r1str=f1r1str.split("/")
                f1r1_tot_str=f1r1str[1]#attr
                f1r1_sig_str=f1r1str[0]#attr

                f2r1str=round1str[1].text.strip()
                f2r1str=f2r1str.split("/")
                f2r1_tot_str=f2r1str[1]#attr
                f2r1_sig_str=f2r1str[0] #attr
            else:
                f1r1_tot_str=None
                f1r1_sig_str=None
                f2r1_tot_str=None
                f2r1_sig_str=None

            round1tkd=round_cards[0].find("span", class_="ufc-round__chip")
            if(round1tkd):
                round1tkd=round1tkd.text.strip()
                round1tkd=round1tkd.split()
                round1tkd=round1tkd[1].split("-")
                f1r1tkd=round1tkd[0] #attr
                f2r1tkd=round1tkd[1] #attr
            else:
                f1r1tkd=None
                f2r1tkd=None
            #round2
            if(round1str):
                f1r2str=round1str[0].text.strip()
                f1r2str=f1r2str.split("/")
                f1r2_tot_str=f1r2str[1]#attr
                f1r2_sig_str=f1r2str[0]#attr

                f2r2str=round1str[1].text.strip()
                f2r2str=f2r2str.split("/")
                f2r2_tot_str=f2r2str[1]#attr
                f2r2_sig_str=f2r2str[0] #attr
            else:
                f1r2_tot_str=None
                f1r2_sig_str=None
                f2r2_tot_str=None
                f2r2_sig_str=None

            round2tkd=round_cards[1].find("span", class_="ufc-round__chip")
            if(round2tkd):
                round2tkd=round2tkd.text.strip()
                round2tkd=round2tkd.split()
                round2tkd=round2tkd[1].split("-")
                f1r2tkd=round2tkd[0] #attr
                f2r2tkd=round2tkd[1] #attr
            else:
                f1r2tkd=None
                f2r2tkd=None
            #round3
            if(round1str):
                f1r3str=round1str[0].text.strip()
                f1r3str=f1r3str.split("/")
                f1r3_tot_str=f1r3str[1]#attr
                f1r3_sig_str=f1r3str[0]#attr

                f2r3str=round1str[1].text.strip()
                f2r3str=f2r3str.split("/")
                f2r3_tot_str=f2r3str[1]#attr
                f2r3_sig_str=f2r3str[0] #attr
            else:
                f1r3_tot_str=None
                f1r3_sig_str=None
                f2r3_tot_str=None
                f2r3_sig_str=None
            
            round3tkd=round_cards[2].find("span", class_="ufc-round__chip")
            if(round3tkd):
                round3tkd=round3tkd.text.strip()
                round3tkd=round3tkd.split()
                round3tkd=round3tkd[1].split("-")
                f1r3tkd=round3tkd[0] #attr
                f2r3tkd=round3tkd[1] #attr
            else:
                f1r3tkd=None
                f2r3tkd=None
            #round4
            if(round1str):
                f1r4str=round1str[0].text.strip()
                f1r4str=f1r4str.split("/")
                f1r4_tot_str=f1r4str[1]#attr
                f1r4_sig_str=f1r4str[0]#attr

                f2r4str=round1str[1].text.strip()
                f2r4str=f2r4str.split("/")
                f2r4_tot_str=f2r4str[1]#attr
                f2r4_sig_str=f2r4str[0] #attr
            else:
                f1r4_tot_str=None
                f1r4_sig_str=None
                f2r4_tot_str=None
                f2r4_sig_str=None
            
            round4tkd=round_cards[3].find("span", class_="ufc-round__chip")
            if(round4tkd):
                round4tkd=round4tkd.text.strip()
                round4tkd=round4tkd.split()
                round4tkd=round4tkd[1].split("-")
                f1r4tkd=round4tkd[0] #attr
                f2r4tkd=round4tkd[1] #attr
            else:
                f1r4tkd=None
                f2r4tkd=None
            #round5
            if(round1str):
                f1r5str=round1str[0].text.strip()
                f1r5str=f1r1str.split("/")
                f1r5_tot_str=f1r5str[1]#attr
                f1r5_sig_str=f1r5str[0]#attr

                f2r5str=round1str[1].text.strip()
                f2r5str=f2r5str.split("/")
                f2r5_tot_str=f2r5str[1]#attr
                f2r5_sig_str=f2r5str[0] #attr
            else:
                f1r5_tot_str=None
                f1r5_sig_str=None
                f2r5_tot_str=None
                f2r5_sig_str=None

            round5tkd=round_cards[4].find("span", class_="ufc-round__chip")
            if(round5tkd):
                round5tkd=round5tkd.text.strip() #attr
                round5tkd=round5tkd.split()
                round5tkd=round5tkd[1].split("-")
                f1r5tkd=round5tkd[0] #attr
                f2r5tkd=round5tkd[1] #attr
            else:
                f1r5tkd=None
                f2r5tkd=None