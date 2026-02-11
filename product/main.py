from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from . import schema
from .import model
from .database import engine,SessionLocal


app = FastAPI()

model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/product')
def product(product: schema.Product, db : Session = Depends(get_db)):
    new_product = model.Product(
        name=product.name, description=product.description, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return product
