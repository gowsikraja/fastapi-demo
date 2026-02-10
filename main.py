from fastapi import FastAPI
from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    name: str
    type: str


myapp = FastAPI()


@myapp.get('/')
def index():
    return 'Hello world'


@myapp.get('/prperty/{id}')
def property(id):
    return f'This is property page of {id}'


@myapp.get('/movies')
def movies():
    return {'movies': [
        {'Movie1', 'action'},
        {'Movie2', 'love'}
    ]}


@myapp.post('/movies')
def getMovies(movie: Movie):
    return movie
