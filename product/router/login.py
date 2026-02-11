from fastapi import APIRouter, Depends, HTTPException, status
from ..import schema, model
from passlib.context import CryptContext
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Login'])

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

SECRET_KEY = '5fe6456aaea7d34ed980235568e1478a1848b0c03030ff5268d40957b0647684'
ALGORITHM = 'HS256'
EXPIRE_TIME = 20  # mins

oath = OAuth2PasswordBearer(tokenUrl='login')


def get_token(data: dict):
    to_token = data.copy()
    expire = datetime.now() + timedelta(minutes=EXPIRE_TIME)
    to_token.update({
        'exp': expire
    })
    encode_jwt = jwt.encode(to_token, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
        'message': 'Logged-in successfully',
        'access_token': token
    }


def get_user(token: str = Depends(oath)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    try:
        decode_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username = decode_token.get('sub')
        if not username:
            raise credential_exception
    except JWTError:
        raise credential_exception
