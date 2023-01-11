from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi import Body, Path, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token, validate_token

app = FastAPI()
app.title = "Netflix API"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "mail@endybits.dev" or data['password'] != "coding123":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")


class User(BaseModel):
    email: str
    password: str
    class Config:
        schema_extra = {
            "example": {
                "email": "mail@endybits.dev",
                "password": "coding123"
            }
        }

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
                "seasons": 4
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


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'mail@endybits.dev' and user.password=='coding123':
        token = create_token(jsonable_encoder(user))
        print(validate_token(token))
        return JSONResponse(content=token, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)



##### SERIES ######

@app.get('/series', tags=['series'], response_model= List[Serie])
def get_serie_list() -> List[Serie]:
    return JSONResponse(content=series)



@app.post('/series/', tags=['series'], response_model=dict, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_serie(
    serie: Serie
) -> dict:
    series.append({
        "id": serie.id,
        "title": serie.title,
        "category": serie.category,
        "year": serie.year,
        "season": serie.seasons
    })
    return JSONResponse(content={"message": "Object Created successfully"}, status_code=status.HTTP_201_CREATED)



@app.get('/series/', tags=['series'], response_model=List[Serie], status_code=status.HTTP_200_OK)
def get_serie_by_category(
    category: str = Query(min_length=4)
) -> List[Serie]:
    data = [serie for serie in series if serie['category'] == category]
    if data:
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    return JSONResponse(content=[], status_code=status.HTTP_400_BAD_REQUEST)



@app.get('/series/{id}', tags=['series'], response_model=Serie, status_code=status.HTTP_200_OK)
def get_serie(
    id: int = Path(..., ge=1)
) -> Serie:
    for serie in series:
        if serie['id'] == id:
            return JSONResponse(content=serie, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Object not found"}, status_code=status.HTTP_400_BAD_REQUEST)



@app.put('/series/{id}', tags=['series'], response_model=dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def update_serie(
    serie: Serie,
    id: int = Path(..., ge=1),
) -> dict:
    for item in series:
        if item['id'] == id:
            item['title'] = serie.title
            item['category'] = serie.category
            item['year'] = serie.year
            item['seasons'] = serie.seasons
            return JSONResponse(content={"message": "Object updated successfully"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Object not found"}, status_code=status.HTTP_400_BAD_REQUEST)



@app.delete('/series/{id}', tags=['series'], response_model= dict, status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def delete_serie(
    id: int = Path(..., ge=1)
) -> dict:
    for serie in series:
        if serie['id'] == id:
            series.remove(serie)
            return JSONResponse(content={"message": "Object deleted successfully"}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Object not found"}, status_code=status.HTTP_400_BAD_REQUEST)