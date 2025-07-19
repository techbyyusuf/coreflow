from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from models.user import User
from security.token_utils import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        user = db.scalars(select(User).where(User.email == email)).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")


def require_admin(user: User = Depends(get_current_user)):
    if user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user


def require_employee(user: User = Depends(get_current_user)):
    if user.role.value not in ["ADMIN", "EMPLOYEE"]:
        raise HTTPException(status_code=403, detail="Employee privileges required")
    return user


def require_viewer(user: User = Depends(get_current_user)):
    return user


def require_self_or_admin(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    print(
        f"Current user: {current_user.id} - Target user: {user_id} - Role: {current_user.role}")
    if current_user.role.value != "ADMIN" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    return current_user
