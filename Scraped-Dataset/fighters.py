from bs4 import BeautifulSoup
import requests
import json

#Part 1: Scrape the basic figther data from the fighters page on UFC stats
fighters_url=[]
letters = 'abcdefghijklmnopqrstuvwxyz'
for letter in letters:
    url=f'http://ufcstats.com/statistics/fighters?char={letter}'
    page=requests.get(url)
    if(page.status_code!=200):
        print(f'Error fetching page data')
        exit()

    soup=BeautifulSoup(page.text, 'html.parser')
    rows=soup.find_all('tr', class_="b-statistics__table-row")
    i=0
    for row in rows[1:]:
        link=row.find('a')
        cols=row.find_all('td')
        # Validate that link exists and cols has enough elements
        if link is None or len(cols)<10: 
            continue
        
        fighter_url={
            'fighter_id': i,
            'fighter_url': link['href'] ,
            'name': cols[0].text.strip()+' '+cols[1].text.strip(),
            'height': cols[3].text.strip(),
            'weight': cols[4].text.strip(),
            'reach': cols[5].text.strip(),
            'stance': cols[6].text.strip(),
            'wins': cols[7].text.strip(),
            'losses': cols[8].text.strip(),
            'draws': cols[9].text.strip()
        }
        i+=1
        fighters_url.append(fighter_url)
#print(fighters_url)

with open('fighters.json', 'w') as f:
    json.dump(fighters_url, f, indent=4)
