from fastapi import APIRouter, Depends, HTTPException, status
from ..import schema, model
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError

router = APIRouter(tags=['Login'])

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

SECRET_KEY = '5fe6456aaea7d34ed980235568e1478a1848b0c03030ff5268d40957b0647684'
ALGORITHM = 'HS256'
EXPIRE_TIME = 20  # mins


def get_token(data: dict):
    to_token = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_TIME)
    to_token.update({
        'exp': expire
    })
    encode_jwt = jwt.encode(to_token, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


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
    token = get_token({
        'sub': seller.username
    })
    return {
        'message':'Logged-in successfully',
        'access_token': token
    }
