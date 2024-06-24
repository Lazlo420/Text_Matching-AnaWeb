import requests
from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

links=[]
with open("links_peru21.txt","r",encoding="utf-8") as file:
    for line in file:
        links.append(line.replace('\n',''))

#algunas entradas se repitieron, me imagino que por la compaginacion de varias ejecuciones accidentadas
links=list(set(links))
revisar=[]
#funcion para evitar molestias
def remove_scripts(soup):
    for script in soup(["script", "style"]):
        script.extract()

def fetch_content(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        remove_scripts(soup)

        headline_tag = soup.find('h1', itemprop='name')
        headline = headline_tag.text.strip() if headline_tag else ''

        article_body = soup.find('div', class_='story-contents__content').text

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

        return(link, headline.replace('\n', ''), bajada.replace('\n', ''), antetitulo.replace('\n', ''), article_body.replace('\n', '').replace("\r",""), date, tags_str)
    except Exception as e:
        print(f"Error processing {link}: {e}")
        revisar.append(link)
        return None

with ThreadPoolExecutor() as executor, open("peru21.csv", 'w', encoding='UTF-8') as doc_csv:
    doc_csv.write("link^^headline^^bajada^^antetitulo^^cuerpo^^dia^^etiquetas\n")
    for result in executor.map(fetch_content, links):
        if result:
            doc_csv.write(f"{'^^'.join(result)}\n")
        
with open("revisar.txt","w",encoding="utf-8") as rev:
    for link in revisar:
        rev.write(link,'\n')