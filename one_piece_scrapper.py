from bs4 import BeautifulSoup
import requests
from tinydb import TinyDB, Query
import re

db = TinyDB('one_piece_db.json', indent=4, ensure_ascii=False)
INFORMATION = db.table('informations')
MANGA = db.table('chapters')

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36 Edg/105.0.1343.33'
}


def get_informations(url: str):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    infos = soup.find('dl', class_='dl-horizontal')

    author = infos.findAll('dd')
    release_date = infos.findAll('dd')
    category = infos.findAll('dd')
    resume = soup.find('div', class_='well').p

    INFORMATION.insert({'author': author[2].text.replace('\n', ''),
                        'resume': resume.text,
                        'release-date': release_date[3].text,
                        'categories':
                            category[4].text.replace('\n', '').split(', ')})


get_informations('https://www.scan-vf.net/one_piece')

CHAPTERS = {}


def get_all_chapters(url: str):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    chapters = soup.find('ul', class_='chapters')
    all_chapters = chapters.findAll('a')

    for src in all_chapters:
        links = src['href']
        response = requests.get(links, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # get chapter number and name from page header
        chapter_name = soup.find('div', class_='page-header').find('b').text
        match = re.search(r'#(\d+)\s*:\s*(.*)', chapter_name)
        if match:
            chapter_number = match.group(1)
            chapter_name = match.group(2)
        else:
            chapter_number = None

        # get images
        images_class = soup.findAll('img', class_='img-responsive')
        IMAGES = []
        for img_src in images_class:
            image_extracted = img_src.get('data-src')

            IMAGES.append(image_extracted) if image_extracted is not None\
                else print('')

            if image_extracted is not None:
                print(f'\rExtraction de l\'image de {image_extracted} ...')

        id_doc = MANGA.insert({'number': chapter_number, 'name': chapter_name, 'pages': IMAGES})
        chapter = MANGA.get(doc_id=id_doc)
        MANGA.update({'id': chapter_number}, Query().id == chapter.doc_id and Query().id != chapter_number)

get_all_chapters('https://www.scan-vf.net/one_piece')
