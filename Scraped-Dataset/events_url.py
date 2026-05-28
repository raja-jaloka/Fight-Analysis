from bs4 import BeautifulSoup
import requests
import json 

events_url=[]
root_url="https://sports-statistics.com/"
url='https://sports-statistics.com/ufc/ufc-fight-statistics/'
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36"
}

page=requests.get(url, headers=headers)
if(page.status_code!=200):
    print(f'Error {page.status_code} fetching page data')
    exit()

soup=BeautifulSoup(page.text, 'html.parser')
year_archives=soup.find_all('ul', class_="ufc-archive__list")
i=0
for archive in year_archives:
    rows=archive.find_all('li')
    for row in rows:
        link=row.find('a')
        link=link['href']
        link=link.strip()
        link=root_url+link
        event={
            "event_id":i,
            "event_url":link
        }
        events_url.append(event)
        i+=1
        print(event)

with open('events_url.json','w') as f:
    json.dump(events_url,f, indent=4)
