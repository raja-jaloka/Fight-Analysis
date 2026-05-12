import requests
import json
from bs4 import BeautifulSoup

with open('Extra_fighters_url.json') as f:
    urls=json.load(f)

fighter_stats=[]

for url in urls:
    fighter_id=url['fighter_id']
    furl=url['furl']
    page=requests.get(furl)
    if(page.status_code!=200):
        print(f'{page.status_code} Error! Can\'t fetch data for fighter {fighter_id}')
        exit()

    soup=BeautifulSoup(page.text, 'html.parser')
    profile_tags=soup.find_all('p', class_="hero-profile__tag")
    f_status=profile_tags[1].text() #attr
    f_div=profile_tags[0].text() #attr
    f_name=soup.find('h1',class_="hero-profile__name")
    f_name=f_name.text() #attr
    f_rec=soup.find('p', class_="hero-profile__division-body") #attr

    rows=soup.find_all('div', class_="stats-records stats-records--two-column") #2-columned-section

    svg=rows[0].find('svg', class_="e-chart-circle")
    title=svg.find('text',class_="e-chart-circle__percent")
    str_acc='0.'+title[:len(title)-1] #attr
    svg=rows[1].find('svg', class_="e-chart-circle")
    title=svg.find('text',class_="e-chart-circle__percent")
    tkd_acc='0.'+title[:len(title)-1] #attr
    grp1=rows[2].find_all('div', class_="c-stat-compare__group c-stat-compare__group-1 ")
    grp2=rows[2].find_all('div', class_="c-stat-compare__group c-stat-compare__group-2 ")
    sig_str=grp1[0].find('div', class_="c-stat-compare__number")
    sig_str_lnd=sig_str.text().strip() #attr
    tkd_avg=grp1[1].find('div', class_="c-stat-compare__number")
    tkd_avg=tkd_avg.text().strip() #attr
    sig_str_abs=grp2[0].find('div', class_="c-stat-compare__number")
    sig_str_abs=sig_str_abs.text().strip() #attr
    sub_avg=grp2[1].find('div', class_="c-stat-compare__number")
    sub_avg=sub_avg.text().strip() #attr

    grp1=rows[3].find_all('div', class_="c-stat-compare__group c-stat-compare__group-1 ")
    grp2=rows[3].find_all('div', class_="c-stat-compare__group c-stat-compare__group-2 ")
    sig_str_def=grp1[0].find('div', class_="c-stat-compare__number")
    sig_str_def=sig_str_def.text().strip() #attr
    kkd_avg=grp1[1].find('div', class_="c-stat-compare__number")
    kkd_avg=kkd_avg.text().strip() #attr
    tkd_def=grp2[0].find('div', class_="c-stat-compare__number")
    tkd_def=tkd_def.text().strip() #attr
    avg_ft=grp2[1].find('div', class_="c-stat-compare__number")
    avg_ft=avg_ft.text().strip() #attr

    rows_2=soup.find_all('div', class_="stats-records stats-records--three-column") #3-columned-section

    rows2_inner=rows_2[0].find_all('div', class_="c-stat-3bar__group")
    sig_str_standing=rows2_inner[0].find('div', class_="c-stat-3bar__value")
    sig_str_standingl=sig_str_standing.text().split('(')
    sig_str_standing=sig_str_standingl[0] #attr
    sig_str_clinch=rows2_inner[1].find('div', class_="c-stat-3bar__value")
    sig_str_clinchl=sig_str_clinch.text().split('(')
    sig_str_clinch=sig_str_clinchl[0] #attr
    sig_str_ground=rows2_inner[2].find('div', class_="c-stat-3bar__value")
    sig_str_groundl=sig_str_standing.text().split('(')
    sig_str_ground=sig_str_groundl[0] #attr

    body_dig=rows_2[1].find('div', class_="c-stat-body__diagram")
    head_str=body_dig.find('g', id="e-stat-body_x5F__x5F_head-txt")
    head_str=head_str.find(id="e-stat-body_x5F__x5F_head_value").text() #attr
    body_str=body_dig.find('g', id="e-stat-body_x5F__x5F_body-txt")
    body_str=body_str.find(id="e-stat-body_x5F__x5F_body_value").text() #attr
    leg_str=body_dig.find('g', id="e-stat-body_x5F__x5F_leg-txt")
    leg_str=leg_str.find(id="e-stat-body_x5F__x5F_leg_value").text() #attr
    
    wins_rows=rows[2].find_all('div', class_="c-stat-3bar__group")
    kol=wins_rows[0].find('div', class_="c-stat-3bar__value")
    kol=kol.text().split('(')
    ko=kol[0] #attr
    decl=wins_rows[1].find('div', class_="c-stat-3bar__value")
    decl=decl.text.split('(')
    dec=decl[0] #attr 
    subl=wins_rows[2].find('div', class_="c-stat-3bar__value")
    subl=subl.text.split('(')
    sub=subl[0] #attr