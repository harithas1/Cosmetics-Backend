from datetime import timedelta, datetime, timezone
from http.client import HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Schema
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import schemas

from database import Session_local
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix = "/auth", tags=['auth']
)

SECRET_KEY = '68f4cf1351c81cd88da54abdb33801f1b156b3fd026a8b9e6f6d887950168b02'
ALGORITHM = 'HS256'


bcrypt_context =  CryptContext(schemes=['bcrypt'],deprecated = 'auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class Token(BaseModel):
    access_token: str
    token_type: str

# DB dependency
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str,password: str, db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return  False
    return user

def  create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta):
    encode = {'sub':username,'user_id':user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('user_id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username':username, 'user_id':user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: schemas.CreateUserRequest):

    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
        role = 'user',
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number = create_user_request.phone_number
    )

    if not create_user_model:
        raise HTTPException

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],db: db_dependency ):
    user = authenticate_user(form_data.username, form_data.password, db)
    # print("user",user.name)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    token = create_access_token(user.username,str(user.user_id), user.role, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}

