from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..import schema, model
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter(tags=['Seller'])

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


@router.post('/seller')
def seller(request: schema.Seller, db: Session = Depends(get_db)):
    hash_psw = pwd_context.hash(request.password)
    seller = model.Seller(username=request.username,
                          email=request.email, password=hash_psw)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
