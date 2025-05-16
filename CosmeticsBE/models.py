from CosmeticsBE.database import Base
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(),unique=True)
    phone_number = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role =  Column(String, default='user')

class Categories(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    image = Column(String)

class Products(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    categoryId = Column(Integer, ForeignKey("categories.category_id"))
    description = Column(String)
    image = Column(JSON)
    brand = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    featured = Column(Boolean, default=False)

class Cart(Base):
    __tablename__ = "cart"
    cart_id = Column(Integer, primary_key=True, index=True)
    userId =  Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)

class CartItem(Base):
    __tablename__ = "cart_item"
    id = Column(Integer, primary_key=True, index=True)
    cartId = Column(Integer, ForeignKey("cart.cart_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)



class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id =  Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)


class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True, index=True)
    orderId = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    # user_id =  Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    name = Column(String(50),nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    image = Column(String,nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime(timezone=True), server_default=func.now())






