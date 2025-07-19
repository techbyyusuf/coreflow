from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str = "VIEWER"

class UserUpdateEmailSchema(BaseModel):
    new_email: str

class UserUpdatePasswordSchema(BaseModel):
    new_password: str
