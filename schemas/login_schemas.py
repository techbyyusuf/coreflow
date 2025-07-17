from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    email: str
    password: str
