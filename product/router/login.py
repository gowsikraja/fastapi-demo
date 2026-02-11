from fastapi import APIRouter, Depends, HTTPException, status
from ..import schema, model
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Login'])

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


@router.post('/login')
def login(request: schema.LoginRequest, db: Session = Depends(get_db)):
    seller = db.query(model.Seller).filter(
        model.Seller.username == request.username).first()

    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Username/Password')

    return 'Logged in successfully'
