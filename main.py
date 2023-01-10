from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Body, Path, Query


app = FastAPI()
app.title = "Netflix API"
app.version = "0.0.1"


id: int = Body(),

class Serie(BaseModel):
    id: Optional[int] = Field(ge=1)
    title: str = Field(..., max_length=40, min_length=2)
    category: str = Field(..., max_length=40, min_length=2)
    year: int = Field(default=2022, le=2022)
    seasons: int = Field(ge=1)

    class Config:
        schema_extra = {
            "example": {
                "id": 10,
                "title": "Prueba",
                "category": "Action",
                "year": 2021,
                "season": 4
            }
        }



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


#### ROUTES #####
@app.get('/', tags=['home'])
def home():
    return {"message": "Hi, FastAPI...!"}


##### SERIES ######
@app.get('/series', tags=['series'], response_model= List[Serie])
def get_serie_list() -> List[Serie]:
    return JSONResponse(content=series)


@app.post('/series/', tags=['series'])
def create_serie(
    serie: Serie
):
    series.append({
        "id": serie.id,
        "title": serie.title,
        "category": serie.category,
        "year": serie.year,
        "season": serie.seasons
    })
    return series


@app.get('/series/', tags=['series'], response_model=List[Serie])
def get_serie_by_category(
    category: str = Query(min_length=4)
) -> List[Serie]:
    data = [serie for serie in series if serie['category'] == category]
    return JSONResponse(content=data)


@app.get('/series/{id}', tags=['series'], response_model=Serie)
def get_serie(
    id: int = Path(..., ge=1)
) -> Serie:
    for serie in series:
        if serie['id'] == id:
            return JSONResponse(content=serie)
    return JSONResponse(content={"message": "Object not found"})


@app.put('/series/{id}', tags=['series'], response_model=Dict)
def update_serie(
    serie: Serie,
    id: int = Path(..., ge=1),
) -> Dict:
    for item in series:
        if item['id'] == id:
            item['title'] = serie.title
            item['category'] = serie.category
            item['year'] = serie.year
            item['seasons'] = serie.seasons
            return JSONResponse(content={"message": "Object updated successfully"})
    return JSONResponse(content={"message": "Object not found"})

@app.delete('/series/{id}', tags=['series'], response_model= Dict)
def delete_serie(
    id: int = Path(..., ge=1)
) -> Dict:
    for serie in series:
        if serie['id'] == id:
            series.remove(serie)
            return JSONResponse(content={"message": "Object deleted successfully"})
    return JSONResponse(content={"message": "Object not found"})