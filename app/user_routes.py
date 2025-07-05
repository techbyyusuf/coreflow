from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.user_service import UserService
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()

@router.post("/")
def create_user(first_name: str, last_name: str, email: str, password: str, db: Session = Depends(get_db)):
    service = UserService(db)
    service.create_user(first_name, last_name, email, password)
    return {"message": "User created successfully."}

