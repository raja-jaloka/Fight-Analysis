import json
import requests
from bs4 import BeautifulSoup

#Part 2: Scrape the detailed fighter data from each fighter's page on UFCstats
fighter_stats=[]

with open('fighters.json', 'r') as f:
    fighters_url=json.load(f)
print(fighters_url) 

'''for fighter in fighters_url:
    fighter_url=fighter['fighter_url']
    page=requests.get(fighter_url)
    if(page.status_code!=200):
        print(f'{page.status_code} Error fetching page data for {fighter_url}')
        exit()
    soup=BeautifulSoup(page.text, 'html.parser')'''

