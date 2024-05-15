import time
from urllib.parse import urlunparse
from bs4 import BeautifulSoup
import datetime as dt
from selenium import webdriver

start = 736330
base_url = 'https://peru21.pe/archivo/todas/'
registro = {}
date = dt.date.fromordinal(736330)
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

def fetch_links(date, driver):
    compilao = []
    complete_url = base_url + str(date) + '/'
    driver.get(complete_url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    updated_html = driver.page_source
    updated_soup = BeautifulSoup(updated_html, 'html.parser')
    link_elements = updated_soup.find_all('a', class_='story-item__title')
    if link_elements:
        for tag in link_elements:
            link = tag.attrs['href']
            if not link.startswith('https://peru21.pe'):
                link = urlunparse(('https', 'peru21.pe', link, '', '', ''))
            compilao.append(link)

    registro[date] = compilao
    print(f'{date} - {len(compilao)} links')


while start < 736695:
    date = dt.date.fromordinal(start)
    fetch_links(date,driver)
    start += 1

with open("links_peru21.txt", "a") as file:
    for i in registro.keys():
        for j in registro[i]:
            file.write(f'{j}\n')

        