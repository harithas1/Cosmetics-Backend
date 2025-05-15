from pydantic import BaseModel,EmailStr

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str


