from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..import schema, model
from ..database import get_db
from passlib.context import CryptContext
from .login import get_user
from typing import List

router = APIRouter(tags=['Seller'])

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


@router.get('/seller', response_model=List[schema.DisplaySeller])
def getSeller(db: Session = Depends(get_db), user: schema.Seller = Depends(get_user)):
    seller = db.query(model.Seller).all()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='No sellers available')
    return seller


@router.post('/seller')
def seller(request: schema.Seller, db: Session = Depends(get_db), user: schema.Seller = Depends(get_user)):
    hash_psw = pwd_context.hash(request.password)
    seller = model.Seller(username=request.username,
                          email=request.email, password=hash_psw)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
