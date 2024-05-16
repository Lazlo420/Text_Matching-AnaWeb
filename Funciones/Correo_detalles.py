import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os

links=[]
with open("Links/links_correo.txt","r",encoding="utf-8") as file:
    for line in file:
        links.append(file.readline().replace('\n',''))
print(len(links))
i=1

def remove_scripts(soup):
    for script in soup(["script", "style"]):
        script.extract()

def extract_data(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove scripts
        remove_scripts(soup)

        headline_tag = soup.find('h1', itemprop='name')
        headline = headline_tag.text.strip() if headline_tag else ''

        paragraphs = soup.find_all('p', itemprop='description')
        article_body = ' '.join(paragraph.text.strip() for paragraph in paragraphs)

        date_tag = soup.find('time')
        date = date_tag['datetime'] if date_tag else ''
        try:
            date = datetime.fromisoformat(date).strftime('%d-%m-%Y')
        except ValueError:
            try:
                date = datetime.strptime(date, '%a %b %d %Y %H:%M:%S GMT%z (%Z)').strftime('%d-%m-%Y')
            except ValueError:
                pass

        tags_tag = soup.find('div', class_='st-tags__box')
        if not tags_tag:
            tags_tag=soup.find('div', class_='story-tags')
        tags = set(tag.text for tag in tags_tag.find_all('a')) if tags_tag else set()
        tags_str = ', '.join(tags)

        bajada_tag = soup.find('h2', class_='sht__summary')
        bajada = bajada_tag.text.strip() if bajada_tag else ''

        antetitulo_tag = soup.find('div', class_='st-social f just-between')
        antetitulo = antetitulo_tag.text.strip() if antetitulo_tag else ''

        return (link, headline, bajada, antetitulo, article_body.replace('\n', '').replace("\r",""), date, tags_str)
    except Exception as e:
        print(f"Error processing {link}: {e}")
        return None

with ThreadPoolExecutor() as executor, open("correo.csv", 'w', encoding='UTF-8') as doc_csv:
    doc_csv.write("link^^headline^^bajada^^antetitulo^^cuerpo^^dia^^etiquetas\n")
    for result in executor.map(extract_data, links):
        print(i)
        i=i+1
        if result:
            doc_csv.write(f"^^".join(result) + '\n')
