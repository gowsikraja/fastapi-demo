from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import schema
from .import model
from .database import engine, SessionLocal
from typing import List


app = FastAPI()

model.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/product', status_code=status.HTTP_201_CREATED)
def product(product: schema.Product, db: Session = Depends(get_db)):
    new_product = model.Product(
        name=product.name, description=product.description, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return product


@app.get('/products')
def getProducts(db: Session = Depends(get_db)):
    products = db.query(model.Product).all()
    return products


@app.get('/product/{id}')
def getProduct(id, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    return product


@app.put('/product/{id}')
def update(id, request: schema.Product, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    product.update(request.model_dump())
    db.commit()
    return 'Product successsully updated'


@app.delete('/product/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id==id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    product.delete()
    db.commit()
    return 'Product successsully deleted'

