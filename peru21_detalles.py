import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os

links=[]
with open("links_peru21.txt","r",encoding="utf-8") as file:
    for line in file:
        links.append(file.readline().replace('\n',''))
links

def extract_data(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

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
        tags = set(tag.text for tag in tags_tag.find_all('a')) if tags_tag else set()
        tags_str = ', '.join(tags)

        bajada_tag = soup.find('h2', class_='sht__summary')
        bajada = bajada_tag.text.strip() if bajada_tag else ''

        antetitulo_tag = soup.find('div', class_='st-social f just-between')
        antetitulo = antetitulo_tag.text.strip() if antetitulo_tag else ''

        return (link, headline.replace('\n', ''), bajada.replace('\n', ''), antetitulo.replace('\n', ''), article_body.replace('\n', ''), date, tags_str)
    except Exception as e:
        print(f"Error processing {link}: {e}")
        return None

with ThreadPoolExecutor() as executor, open("peru21.csv", 'a', encoding='UTF-8') as doc_csv:
    for result in executor.map(extract_data, links):
        if result:
            doc_csv.write(f"{';'.join(result)}\n")
        