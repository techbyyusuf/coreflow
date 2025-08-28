from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    """
    Schema for user login.
    """
    email: str
    password: str
