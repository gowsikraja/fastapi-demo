from fastapi import FastAPI
from .schema import Product
from .import model
from .database import engine


app = FastAPI()

model.Base.metadata.create_all(engine)


@app.post('/product')
def product(product: Product):
    return product
