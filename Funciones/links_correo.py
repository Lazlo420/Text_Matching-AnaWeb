import requests_html
import datetime as dt
from concurrent.futures import ThreadPoolExecutor

start = 736330
base_url = 'https://diariocorreo.pe/archivo/todas/'
registro = {}

def fetch_links(date):
    complete_url = base_url + str(date) + '/'
    session = requests_html.HTMLSession()
    response = session.get(complete_url)
    link_tags = response.html.find('a.story-item__title')
    if not link_tags:
        print(f'revisar {date}')
    compilao=['https://diariocorreo.pe'+link.attrs["href"] for link in link_tags]
    registro[date] = compilao
    print(f'{date} - {len(compilao)} links')


##--esto si fue claude, no sabia que existia esto xd
with ThreadPoolExecutor() as executor:
    while start < 737060:
        date = dt.date.fromordinal(start)
        executor.submit(fetch_links, date)
        start += 1

with open("links_correo.txt","w") as file:
    for i in registro.keys():
        for j in registro[i]:
            file.write(f'{j}\n')