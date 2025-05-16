from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
import CosmeticsBE.schemas as schemas

from CosmeticsBE.database import Session_local
from CosmeticsBE.models import Products, Cart, CartItem, Orders, OrderItem
from CosmeticsBE.routers.auth import get_current_user

router = APIRouter(
    prefix = "/orders", tags=['orders']
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


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderRequest,user: user_dependency,db: db_dependency):
    userId = user.get('user_id')

    #     Create new Order
    new_order = Orders(user_id = userId)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        product = db.query(Products).filter(Products.product_id==item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID{item.product_id} not found")
        total_price = product.price * item.quantity

        order_item = OrderItem(
            orderId = new_order.order_id,
            product_id = product.product_id,
            name=product.product_name,
            quantity=item.quantity,
            image=product.image[0] if product.image[0] else product.image[1],
            total_price=total_price
        )
        db.add(order_item)
    db.commit()
    return {"message": "Order created successfully", "order_id": new_order.order_id}


@router.get("/getOrders",status_code=status.HTTP_200_OK)
async def get_orders(user: user_dependency,db:db_dependency):
    user_id = user.get('user_id')
    # Getting user's cart
    orders = db.query(Orders).filter(Orders.user_id==user_id).all()
    print("orders.....",orders)
    if not orders:
        return {"message": "No orders yet"}

    # collecting all order Ids
    order_ids = [order.order_id for order in orders]

    order_items = db.query(OrderItem).filter(OrderItem.orderId.in_(order_ids)).all()

    if not order_items:
        return {"message": "No order items found"}
    return order_items





