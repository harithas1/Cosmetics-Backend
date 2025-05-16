from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import CosmeticsBE.schemas as schemas

from CosmeticsBE.database import Session_local
from CosmeticsBE.models import Products


router = APIRouter(
    prefix = "/products", tags=['products']
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
async def add_products(db: db_dependency, product: schemas.AddProduct):
    # print(product)
    add_product_model = Products(
        product_name = product.product_name,
        description = product.description,
        categoryId = product.categoryId,
        image = product.image,
        brand = product.brand,
        price = product.price,
        quantity = product.quantity,
        featured =product.featured
        )
    db.add(add_product_model)
    db.commit()
    return {
        "message": "Product added successfully",
        "product": add_product_model
    }


@router.get("/getProducts", status_code=status.HTTP_200_OK)
async def get_category(db: db_dependency):
    add_product_model = db.query(Products).all()
    return add_product_model

@router.get("/getProducts/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_detail(db: db_dependency,product_id: int):
    get_product_detail = db.query(Products).filter(Products.product_id==product_id).first()
    return get_product_detail

