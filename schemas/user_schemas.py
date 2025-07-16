from pydantic import BaseModel, EmailStr

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"

class UserUpdateEmailSchema(BaseModel):
    new_email: str

class UserUpdatePasswordSchema(BaseModel):
    new_password: str
