from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from app.dependencies import get_db
from schemas.login_schemas import LoginSchema
from security.token_utils import create_access_token
from security.security import verify_password  # <- Deine eigene Funktion

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login_user(payload: LoginSchema, db: Session = Depends(get_db)):
    stmt  = select(User).where(User.email == payload.email)
    user = db.scalars(stmt).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "role": str(user.role)})
    return {"access_token": token, "token_type": "bearer"}
