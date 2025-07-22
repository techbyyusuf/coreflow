from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    """
    Schema for creating a new user.
    """
    name: str
    email: str
    password: str
    role: str = "VIEWER"

class UserUpdateEmailSchema(BaseModel):
    """
    Schema for updating a user's email.
    """
    new_email: str

class UserUpdatePasswordSchema(BaseModel):
    """
    Schema for updating a user's password.
    """
    new_password: str
