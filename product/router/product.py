from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..import schema, model
from ..database import get_db
from typing import List

router = APIRouter(tags=['Products'], prefix='/product')


@router.post('', status_code=status.HTTP_201_CREATED)
def product(product: schema.Product, db: Session = Depends(get_db)):
    new_product = model.Product(
        name=product.name, description=product.description, price=product.price, seller_id=1)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return product


@router.get('', response_model=List[schema.DisplayProduct])
def getProducts(db: Session = Depends(get_db)):
    products = db.query(model.Product).all()
    return products


@router.get('/{id}')
def getProduct(id, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    return product


@router.put('/{id}')
def update(id, request: schema.Product, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

    product.update(request.model_dump())
    db.commit()
    return 'Product successsully updated'


@router.delete('/{id}')
def delete(id, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id)
    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    product.delete()
    db.commit()
    return 'Product successsully deleted'
