import json
import requests
import sys
from bs4 import BeautifulSoup

UFC_events=[]
sys.stdout.reconfigure(encoding='utf-8')

root="https://sports-statistics.com"

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0 Safari/537.36"
}
with open('events_url.json', 'r') as f:
    events_url=json.load(f)

for url in events_url:
    eurl=url['event_url']
    event_id=url['event_id']
    page=requests.get(eurl, headers=headers)
    if(page.status_code!=200):
        print(f"Failed to fetch {eurl}")
        exit()
    soup=BeautifulSoup(page.text, 'html.parser')
    event_detail=soup.find('div', class_="ufc-event-hero__inner")
    if(event_detail):
        event_title=event_detail.find('h1', class_="ufc-event-hero__title")
        if(event_title):
            event_title=event_title.text.strip() #attr
        else:
            event_title=None
    else:
        event_title=None
    
    event=[]
    #events={}
    card_blocks=soup.find_all('section', class_="ufc-card-block")
    if(card_blocks):
        for card_block in card_blocks:
            fights=card_block.find_all('li', class_="ufc-fight")
            if(fights):
                for fight in fights:
                    fight_link=fight.find('a', class_="ufc-fight__link")
                    if(fight_link):
                        fight_link=root+fight_link['href'] #attr
                    else:
                        fight_link=None
                    fight_night={
                        "fight_link":fight_link
                    }
                    event.append(fight_night)
    events={
        'event_id': event_id,
        'event_title': event_title,
        'fights':event
    }
    UFC_events.append(events)
    print(events)

with open('fights_per_event.json', 'w') as f:
    json.dump(UFC_events, f, indent=4)