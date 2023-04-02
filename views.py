import json
from tinydb import TinyDB, Query

with open('one_piece_db.json', 'r') as f:
    data = json.load(f)

INFORMATIONS = data['informations']
CHAPTERS = data['chapters']
db = TinyDB('one_piece_db.json', indent=4, ensure_ascii=False)
MANGA = db.table('chapters')


def get_about():
    for name in INFORMATIONS:
        return INFORMATIONS[name]


def get_all_titles():
    return [CHAPTERS[index]['name'] for index in CHAPTERS]


def get_specific_chapter(number: str):
    chapter = MANGA.get(Query().number == number)
    return chapter if chapter is not None \
        else {f'Chapter {number} not found'}


def get_last_chapter():
    return CHAPTERS['1']


def get_last_five_chapters():
    return CHAPTERS[:5]


def get_title_of_chapter(number: str):
    chapter = MANGA.get(Query().number == number)
    return chapter['name'] if chapter is not None \
        else {f'Chapter {number} not found'}


def get_link_adress_of_specific_page(number: str, number_page: str):
    chapter = MANGA.get(Query().number == number)

    if chapter is None:
        return {f'The chapter {number} is not in the database'}

    adresses = [link_adress for link_adress in chapter['pages']]
    for link_adress in adresses:
        if number_page == link_adress.split("/")[-1].split('.')[0]:
            return link_adress
    return {f'The chapter {number} does not have a page {number_page}'}
