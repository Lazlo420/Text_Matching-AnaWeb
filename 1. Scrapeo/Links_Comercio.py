import requests_html
from urllib.parse import urlunparse
import datetime as dt
from concurrent.futures import ThreadPoolExecutor

start = 736330
base_url = 'https://elcomercio.pe/archivo/todas/'
registro = {}

def fetch_links(date):
    compilao = []
    complete_url = base_url + str(date) + '/'
    session = requests_html.HTMLSession()
    response = session.get(complete_url)
    link_tags = response.html.find('a.story-item__title')
    if not link_tags:
        print(f'revisar {date}')
    else:
        for tag in link_tags:
            link = tag.attrs['href']
            if not link.startswith('https://elcomercio.pe'):
                link = urlunparse(('https', 'elcomercio.pe', link, '', '', ''))
            compilao.append(link)
    registro[date] = compilao
    print(f'{date} - {len(compilao)} links')

##--esto si fue claude, no sabia que existia esto xd
with ThreadPoolExecutor() as executor:
    while start < 737060:
        date = dt.date.fromordinal(start)
        executor.submit(fetch_links, date)
        start += 1

with open("links_comercio.txt","w") as file:
    for i in registro.keys():
        for j in registro[i]:
            file.write(f'{j}\n')
            
    
        