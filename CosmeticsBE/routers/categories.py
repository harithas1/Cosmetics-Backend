from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import CosmeticsBE.schemas as schemas

from CosmeticsBE.database import Session_local
from CosmeticsBE.models import Categories, Products

router = APIRouter(
    prefix = "/category", tags=['category']
)


# Token schema
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

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_category(db: db_dependency, add_category: schemas.AddCategory):
    add_category_model = Categories(
        category_name = add_category.category_name,
        image = add_category.image
    )
    db.add(add_category_model)
    db.commit()
    return add_category_model


@router.get("/getCategories", status_code=status.HTTP_200_OK)
async def get_category(db: db_dependency):
    add_category_model = db.query(Categories).all()
    return add_category_model

@router.get("/getProductsById/{category_id}", status_code=status.HTTP_200_OK)
async def get_Products_By_categoryId(db:db_dependency,category_id:int):
    products = db.query(Products).filter(Products.categoryId == category_id).all()
    return products