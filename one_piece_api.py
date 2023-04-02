import uvicorn
from fastapi import FastAPI, Path

from views import get_all_titles, get_about, get_specific_chapter, get_last_chapter, \
        get_last_five_chapters, get_title_of_chapter, get_link_adress_of_specific_page

app = FastAPI()


@app.get('/')
def index():
    return {'message': 'My first Api',
            'about/': 'To get information about manga name',
            'docs/': 'Get the documentation',
            }


# recuperer les informations
@app.get('/about/')
def about():
    return get_about()


# recuperer tous nom des chapitres
@app.get('/chapters/')
def all_titles():
    return get_all_titles()


# Recuperer un chapitre
@app.get('/chapters/{idx}/pages/')
def specific_chapter(idx: str = Path(..., description='Add the index to get the a chapter specifique')):
    return get_specific_chapter(idx)


# Recuperer le dernier chapter
@app.get('/last/')
def last_chapter():
    return get_last_chapter()


@app.get('/chapters/{idx}/title/')
def title_of_chapter(idx: str = Path(..., description='Add the index to get the chapter name')):
    return get_title_of_chapter(idx)


@app.get('/chapters/{idx}/pages/{number_page}/')
def link_adress_of_specific_page(idx: str, number_page: str):
    return get_link_adress_of_specific_page(idx, number_page)


@app.get('/last-five/')
def last_five():
    return get_last_five_chapters()


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
