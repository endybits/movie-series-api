from fastapi import FastAPI
from fastapi import Body

app = FastAPI()
app.title = "Netflix API"
app.version = "0.0.1"


series = [
    {
        "id": 1,
        "title": "Merlina",
        "category": "Fantasy",
        "year": 2022,
        "seasons": 1
    },
        {
        "id": 2,
        "title": "Otra serie",
        "category": "Accion",
        "year": 2022,
        "seasons": 1
    },
        {
        "id": 3,
        "title": "Merlina II",
        "category": "Fantasy",
        "year": 2022,
        "seasons": 1
    }

]

@app.get('/', tags=['home'])
def home():
    return {"message": "Hi, FastAPI...!"}


@app.get('/series', tags=['series'])
def get_serie_list():
    return series


@app.get('/series/{id}', tags=['series'])
def get_serie(
    id: int
):
    for serie in series:
        if serie['id'] == id:
            return serie
    return []


@app.get('/series/', tags=['series'])
def get_serie_by_category(
    category: str
):
    return [serie for serie in series if serie['category'] == category]


@app.post('/series/', tags=['series'])
def create_serie(
    id: int = Body(),
    title: str = Body(),
    category: str = Body(),
    year: int = Body(), 
    seasons: int = Body()
):
    series.append({
        "id": id,
        "title": title,
        "category": category,
        "year": year,
        "season": seasons
    })
    return series



@app.delete('/series/{id}', tags=['series'])
def delete_serie(
    id: int
):
    for serie in series:
        if serie['id'] == id:
            series.remove(serie)
    return series


@app.put('/series/{id}', tags=['series'])
def update_serie(
    id: int,
    title: str = Body(),
    category: str = Body(),
    year: int = Body(), 
    seasons: int = Body()
):
    for serie in series:
        if serie['id'] == id:
            serie['title'] = title
            serie['category'] = category,
            serie['year'] = year,
            serie['seasons'] = seasons,
            return serie

