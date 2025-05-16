from pydantic import BaseModel,EmailStr
from typing import List

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str

class AddCategory(BaseModel):
    category_name: str
    image: str


class AddProduct(BaseModel):
    product_name: str
    description: str
    categoryId: int
    image: List[str]
    brand: str
    price: int
    quantity: int
    featured: bool
