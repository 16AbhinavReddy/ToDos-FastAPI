from fastapi import APIRouter, Depends, status, HTTPException
from models import users
from pydantic import BaseModel
from passlib.context import CryptContext
from database import sessionlocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '668f3c8d2f50b3708e8d887a5e3f42c680435ac641eaa3e82b7dbf7e64716c3b'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated= 'auto')
oaut2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_data() :
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_data)]

class UserRequests(BaseModel) :
    username : str
    emailid : str
    first_name : str
    last_name : str
    password : str
    role : str

class Token(BaseModel) :
    access_token : str
    token_type : str

def authenticate_user(Username : str, Password : str, db) :
    user = db.query(users).filter(users.username == Username).first()
    if not user:
        return False
    if not bcrypt_context.verify(Password, user.hashed_password) :
        return False
    return user

def create_user(Username : str, user_id : int, expires_delta : timedelta) :
    encode = {'sub' : Username, 'id' : user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_curr_user(token : Annotated[str, Depends(oaut2_bearer)]) :
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username / User ID is invalid')
        return {'username' : username, 'user_ID' : user_id}
    except JWTError :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username / User ID is invalid')


@router.post('/', status_code=status.HTTP_201_CREATED)

async def get_auth(db : db_dependency, create_user_requests : UserRequests):
    create_user_model = users(
        emailid = create_user_requests.emailid,
        username = create_user_requests.username,
        first_name = create_user_requests.first_name,
        last_name = create_user_requests.last_name,
        hashed_password = bcrypt_context.hash(create_user_requests.password),
        role = create_user_requests.role,
        is_active = True
    )
    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model=None)

async def login_access_from_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency) ->Token: 
    user = authenticate_user(form_data.username, form_data.password, db) 
    if not user :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Username / User ID is invalid')
    user_token = create_user(user.username, user.id, timedelta(minutes=20))
    return {"access_token" : user_token, "token_type" : "bearer"}




