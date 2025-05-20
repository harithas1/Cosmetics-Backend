from itertools import product
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import schemas

from database import Session_local
from models import Products, Cart, CartItem
from routers.auth import get_current_user

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
    return {
        "message": f"Added product {request.product_id} to cart.",
        "cart_id": cart.cart_id,
        "product_id": request.product_id,
        "quantity": cart_item.quantity
    }


@router.get("/getCartItems",status_code=status.HTTP_200_OK)
async def get_cart_items(user: user_dependency,db:db_dependency):
    user_id = user.get('user_id')
    # Getting user's cart
    cart = db.query(Cart).filter(Cart.userId==user_id).first()
    if not cart:
        return {"message": "No cart found for user. Your cart is empty."}
    # to get all cart items for this cart
    cart_items = db.query(CartItem).filter(cart.cart_id == CartItem.cartId).all()
    if not cart_items:
        return {"message": "Your cart is empty."}
    result =[]
    for item in cart_items:
        product=db.query(Products).filter(Products.product_id == item.product_id).first()
        result.append({
            "cart_item_id": item.id,
            "quantity": item.quantity,
            "product": {
                "id": product.product_id,
                "name": product.product_name,
                "price": product.price,
                "image":product.image,
                "description": product.description,
                "brand": product.brand
                }
            })
    return result



# @router.delete("/cart/remove/{cart_item_id}")
# def remove_from_cart(cart_item_id: int, db: db_dependency, user: user_dependency):
#     cart_item = db.query(CartItem).filter(CartItem.id== cart_item_id).first()
#
#     if not cart_item:
#         raise HTTPException(status_code=404, detail="Cart item not found")
#
#     db.delete(cart_item)
#     db.commit()
#
#     return {"message": "Item removed from cart successfully"}
