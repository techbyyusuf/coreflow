from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.user_service import UserService
from app.dependencies import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_user(first_name: str, last_name: str, email: str, password: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        service.create_user(first_name, last_name, email, password)
        return {"message": "User created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/email")
def update_user_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        service.update_user_email(user_id, new_email)
        return {"message": "Email updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/password")
def update_user_password(user_id: int, new_password: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        service.update_user_password(user_id, new_password)
        return {"message": "Password updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        service.delete_user(user_id)
        return {"message": "User deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
