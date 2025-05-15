from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field

from database import Session_local
from typing import Annotated
from sqlalchemy.orm import Session
from models import Users
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix="/user", tags=['user']
)



# DB dependency
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_current_user_profile(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return db.query(Users).filter(Users.user_id==user.get('user_id')).first()