from fastapi import FastAPI

myapp = FastAPI()


@myapp.get('/')
def index():
    return 'Hello world'


@myapp.get('/movies')
def movies():
    return {'movies': [
        {'Movie1', 'action'},
        {'Movie2', 'love'}
    ]}
