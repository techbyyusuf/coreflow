from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from enum import Enum

from models.user import User
from app.database.session import get_db
from security.token_utils import create_access_token
from security.password_manager import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates a user using email and password.

    Returns:
        A JWT token if credentials are valid.

    Raises:
        HTTPException 401: If credentials are invalid.
    """
    stmt = select(User).where(User.email == form_data.username)
    user = db.scalars(stmt).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user.email,
        "role": user.role.value if isinstance(user.role, Enum) else user.role
    })

    return {"access_token": token, "token_type": "bearer"}
