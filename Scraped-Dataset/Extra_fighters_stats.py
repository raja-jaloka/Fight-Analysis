import requests
import json
from bs4 import BeautifulSoup
import sys
import time 
import socket
sys.stdout.reconfigure(encoding='utf-8') #certain fighter's names have special characters in them.

with open('Extra_fighters_url.json') as f:
    urls=json.load(f)

fighter_stats=[]
failed_fighter=[]

original_getadd_info=socket.getaddrinfo
def force_ipv4(host, port, family=0, type=0, proto=0, flag=0):
    return original_getadd_info(host, port, socket.AF_INET, type, proto, flag) #.AF_INET is for ipv4, AF_INET6 is for ipv6
socket.getaddrinfo = force_ipv4 #NOTE: THIS IS A MONKEY PATCH TO FORCE IPV4

session=requests.Session() #session is used instead of requests because it's faster as it reuses the same connection for multiple requests saving time and cpu utilization

for url in urls:
    fighter_id=url['fighter_id']
    furl=url['furl']
    print(f'===processing fighter {fighter_id}===')

    #page=requests.get(furl) 

    try:
        start1=time.time()
        page=session.get(furl, timeout=(30, 60)) #timeout to avoid hanging on a request for too long
        #page=requests.get(furl) 
        print(f'fetch time: {time.time()-start1:.2f}')

        if(page.status_code!=200):
            print(f'{page.status_code} Error! Can\'t fetch data for fighter {fighter_id}')
            exit()

        start2=time.time()
        soup=BeautifulSoup(page.text, 'html.parser')
        print(f'parsing time: {time.time()-start2:.2f}')

        start3=time.time()

        hero_profimg=soup.find('div', class_="hero-profile__image-wrap")
        if(hero_profimg):
            hero_img=hero_profimg.find('img', class_="hero-profile__image")
            if(hero_img):
                hero_img_url=hero_img['src'] #attr 
            else:
                hero_img_url=None
        else:
            hero_img_url=None

        profile_tags=soup.find_all('p', class_="hero-profile__tag")
        if(len(profile_tags)>1):
            f_status=profile_tags[1].text #attr
            f_div=profile_tags[0].text.strip() #attr
        f_name=soup.find('h1',class_="hero-profile__name")
        if(f_name):
            f_name=f_name.text.strip() #attr
        f_rec=soup.find('p', class_="hero-profile__division-body") #attr
        if(f_rec):
            f_rec=f_rec.text.strip()

        rows=soup.find_all('div', class_="stats-records stats-records--two-column") #2-columned-section

        if(len(rows)<4): #if a fighter stat is incomplete they are most probably not an important fighter/not experienced enough thus skippable.
            fighter_failed={
                'fighter_id':fighter_id,
                'furl':furl,
                'error':'Incomplete stats'
            }
            failed_fighter.append(fighter_failed)
            continue

        svg=rows[0].find('svg', class_="e-chart-circle")
        if svg:
            title = svg.find('text', class_="e-chart-circle__percent")

            if title:
                title = title.text.strip()
                str_acc = float(title.replace('%', '')) / 100
            else:
                str_acc = None
        else:
            str_acc = None #attr
        #title=svg.find('text',class_="e-chart-circle__percent")
        #title=title.text.strip()
        #str_acc='0.'+title[:len(title)-1] #attr
        svg=rows[1].find('svg', class_="e-chart-circle")
        if svg:
            title = svg.find('text', class_="e-chart-circle__percent")

            if title:
                title = title.text.strip()
                tkd_acc = float(title.replace('%', '')) / 100
            else:
                tkd_acc = None
        else:
            tkd_acc = None
        #title=svg.find('text',class_="e-chart-circle__percent")
        #title=title.text.strip()
        #tkd_acc='0.'+title[:len(title)-1] #attr
        grp1=rows[2].find_all('div', class_="c-stat-compare__group c-stat-compare__group-1")
        grp2=rows[2].find_all('div', class_="c-stat-compare__group c-stat-compare__group-2")
        sig_str=grp1[0].find('div', class_="c-stat-compare__number")
        sig_str_lnd=sig_str.text.strip() #attr
        tkd_avg=grp1[1].find('div', class_="c-stat-compare__number")
        tkd_avg=tkd_avg.text.strip() #attr
        sig_str_abs=grp2[0].find('div', class_="c-stat-compare__number")
        sig_str_abs=sig_str_abs.text.strip() #attr
        sub_avg=grp2[1].find('div', class_="c-stat-compare__number")
        sub_avg=sub_avg.text.strip() #attr

        grp1=rows[3].find_all('div', class_="c-stat-compare__group c-stat-compare__group-1")
        grp2=rows[3].find_all('div', class_="c-stat-compare__group c-stat-compare__group-2")
        if(grp1):
            sig_str_def=grp1[0].find('div', class_="c-stat-compare__number")
            if(sig_str_def):
                sig_str_def=sig_str_def.text.strip() #attr
            kkd_avg=grp1[1].find('div', class_="c-stat-compare__number")
            if(kkd_avg):
                kkd_avg=kkd_avg.text.strip() #attr
        
        if(grp2):
            tkd_def=grp2[0].find('div', class_="c-stat-compare__number")
            if(tkd_def):
                tkd_def=tkd_def.text.strip() #attr
            avg_ft=grp2[1].find('div', class_="c-stat-compare__number")
            if(avg_ft):
                avg_ft=avg_ft.text.strip() #attr

        rows_2=soup.find_all('div', class_="stats-records stats-records--three-column") #3-columned-section

        rows2_inner=rows_2[0].find_all('div', class_="c-stat-3bar__group")
        sig_str_standing=rows2_inner[0].find('div', class_="c-stat-3bar__value")
        sig_str_standingl=sig_str_standing.text.strip()
        sig_str_standingl=sig_str_standingl.split('(')
        sig_str_standing=sig_str_standingl[0] #attr
        sig_str_clinch=rows2_inner[1].find('div', class_="c-stat-3bar__value")
        sig_str_clinchl=sig_str_clinch.text.strip().split('(')
        sig_str_clinch=sig_str_clinchl[0] #attr
        sig_str_ground=rows2_inner[2].find('div', class_="c-stat-3bar__value")
        sig_str_groundl=sig_str_ground.text.strip().split('(')
        sig_str_ground=sig_str_groundl[0] #attr

        body_dig=rows_2[1].find('div', class_="c-stat-body__diagram")
        head_str=body_dig.find('g', id="e-stat-body_x5F__x5F_head-txt")
        head_str=head_str.find(id="e-stat-body_x5F__x5F_head_value").text #attr
        body_str=body_dig.find('g', id="e-stat-body_x5F__x5F_body-txt")
        body_str=body_str.find(id="e-stat-body_x5F__x5F_body_value").text #attr
        leg_str=body_dig.find('g', id="e-stat-body_x5F__x5F_leg-txt")
        leg_str=leg_str.find(id="e-stat-body_x5F__x5F_leg_value").text #attr
        
        wins_rows=rows_2[2].find_all('div', class_="c-stat-3bar__group")
        kol=wins_rows[0].find('div', class_="c-stat-3bar__value")
        kol=kol.text.split('(')
        ko=kol[0] #attr
        decl=wins_rows[1].find('div', class_="c-stat-3bar__value")
        decl=decl.text.split('(')
        dec=decl[0] #attr 
        subl=wins_rows[2].find('div', class_="c-stat-3bar__value")
        subl=subl.text.split('(')
        sub=subl[0] #attr

        info_2row=soup.find('div', class_="c-bio__row--2col")
        info_3row=soup.find_all('div', class_="c-bio__row--3col")

        if(info_2row):
            cols2=info_2row.find_all('div', class_="c-bio__field c-bio__field--border-bottom-small-screens")
            if(len(cols2)>1):
                tag=cols2[1].find('div', class_="c-bio__label")
                tag=tag.text.strip()
                tag_style=cols2[1].find('div', class_="c-bio__text")
                tag_style=tag_style.text.strip()
                if(tag=='Fighting style'):
                    fighting_style=tag_style #attr
                else:
                    fighting_style=None
            else:
                fighting_style=None

        if(len(info_3row)>1):
            cols3=info_3row[0].find_all('div', class_="c-bio__field")

            if(len(cols3)>2):
                fields_age=cols3[0].find('div', class_="c-bio__label")
                if(fields_age.text.strip()=='Age'):
                    age=cols3[0].find('div', class_="field field--name-age field--type-integer field--label-hidden field__item")
                    age=age.text.strip() #attr
                else:
                    age=None
                height=cols3[1].find('div', class_="c-bio__text")
                if(height):
                    height=height.text.strip() #attr
                else:
                    height=None
                weight=cols3[2].find('div', class_="c-bio__text")
                if(weight):
                    weight=weight.text.strip() #attr
                else:
                    weight=None
            else:
                age=None
                weight=None
                height=None

            cols31=info_3row[1].find_all('div', class_="c-bio__field")
            if(len(cols31)>2):
                reach=cols31[1].find('div', class_="c-bio__text")
                if(reach):
                    reach=reach.text.strip() #attr
                else:
                    reach=None
                leg_reach=cols31[2].find('div', class_="c-bio__text")
                if(leg_reach):
                    leg_reach=leg_reach.text.strip() #attr 
                else:
                    leg_reach=None
            else:
                reach=None
                leg_reach=None
        
        print(f'data fetching: {time.time()-start3:.2f}')

        fighter_stat={
            'fighter_id':fighter_id,
            'fighter_img_url':hero_img_url,
            'status':f_status,
            'div':f_div,
            'name':f_name,
            'record':f_rec,
            'striking_accuracy':str_acc,
            'takedown_accuracy':tkd_acc,
            'significant_strikes_landed':sig_str_lnd,
            'takedown_average':tkd_avg,
            'sig_str_abs':sig_str_abs,
            'sub_avg':sub_avg,
            'sig_str_def':sig_str_def,
            'kkd_avg':kkd_avg,
            'tkd_def':tkd_def,
            'avg_Fight_time':avg_ft,
            'ss_standing':sig_str_standing,
            'ss_clinch':sig_str_clinch,
            'ss_ground':sig_str_ground,
            'head_str':head_str,
            'body_str':body_str,
            'leg_str':leg_str,
            'KO':ko,
            'Decision':dec,
            'Submissions':sub,
            'style':fighting_style,
            'age':age,
            'height':height,
            'weight':weight,
            'reach':reach,
            'leg_reach':leg_reach
        }
        fighter_stats.append(fighter_stat)
        print(f'Succesfully fetched data for fighter {fighter_id}-{f_name}')
        print('--------------complete---------------')
    
    except requests.exceptions.Timeout as e:
        print(f'Timeout error for fighter {fighter_id}')
        fighter_failed={
            'fighter_id':fighter_id,
            'furl':furl,
            'error':str(e),
            'error_type': type(e).__name__
        }
        failed_fighter.append(fighter_failed)
        continue
    
    except Exception as e:
        print(f'Error for fighter {fighter_id}: {e}')
        fighter_failed={
            'fighter_id':fighter_id,
            'furl':furl,
            'error':str(e), #storing message of the error
            'error_type': type(e).__name__ #storing type of the error
        }
        failed_fighter.append(fighter_failed)
        continue


with open('Extra_fighters_stats.json','w',encoding='utf-8') as f:
    json.dump(fighter_stats,f,indent=4,ensure_ascii=False)
    
