from itertools import product
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import CosmeticsBE.schemas as schemas

from CosmeticsBE.database import Session_local
from CosmeticsBE.models import Products, Cart, CartItem
from CosmeticsBE.routers.auth import get_current_user

router = APIRouter(
    prefix = "/cart", tags=['cart']
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
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/addToCart", status_code=status.HTTP_201_CREATED)
async def add_to_cart(request: schemas.AddToCartRequest,user: user_dependency,db: db_dependency):
    user_id = user.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid user ID")
    cart = db.query(Cart).filter(Cart.userId == user_id).first()
    if not cart:
        cart_model = Cart(userId = user_id)
        db.add(cart_model)
        db.commit()
        db.refresh(cart)
    cart_item = db.query(CartItem).filter(CartItem.cartId == cart.cart_id, CartItem.product_id == request.product_id).first()
    if cart_item:
        cart_item+=request.quantity
    else:
        cart_item = CartItem(
            cartId = cart.cart_id,
            product_id = request.product_id,
            quantity = request.quantity,
        )
        db.add(cart_item)
    db.commit()
    return {"message":"Item added to cart","cart_id":cart.cart_id}



@router.get("/getCartItems",status_code=status.HTTP_200_OK)
async def get_cart_items(user: user_dependency,db:db_dependency):
    user_id = user.get('user_id')
    # Getting user's cart
    cart = db.query(Cart).filter(Cart.userId==user_id).first()
    if not cart:
        return {"message": "No items in cart."}
    # to get all cart items for this cart
    cart_items = db.query(CartItem).filter(cart.cart_id == CartItem.cartId).all()
    if not cart_items:
        return {"message": "Cart is empty."}
    return cart_items
