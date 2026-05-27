import requests
import json
from bs4 import BeautifulSoup

fighter_urls=[]

i=0
for page_no in range(1,285):
    url=f'https://www.ufc.com/athletes/all?page={page_no}'
    page= requests.get(url)
    if(page.status_code!=200):
        print(f'{page.status_code} Error! found at page number:{page_no}')
        exit()
    soup=BeautifulSoup(page.text, "html.parser")
    rows=soup.find_all('li', class_="l-flex__item")
    for row in rows: 
        link=row.find('a', class_="e-button--black")
        if(link is None): #Used to check if a link is even returned or not. Not None type
            continue
        link=f'https://ufc.com{link['href']}'
        fighter_url={
            'fighter_id':i,
            'furl':link
        } 
        i+=1
        fighter_urls.append(fighter_url)
        print(fighter_url)

with open('Extra_fighters_url.json', 'w') as f:
    json.dump(fighter_urls,f,indent=4)
