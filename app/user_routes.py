from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.user_service import UserService
from app.database.session import get_db
from schemas.user_schemas import UserCreateSchema, UserUpdateEmailSchema, UserUpdatePasswordSchema
from models.user import User
from security.dependencies import require_admin, require_self_or_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_all_users(
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Retrieve all users (admin only).
    """
    try:
        service = UserService(db)
        return service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_user(
        payload: UserCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Create a new user (admin only).
    """
    try:
        service = UserService(db)
        service.create_user(
            payload.name,
            payload.email,
            payload.password,
            payload.role
        )
        return {"message": "User created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/email")
def update_user_email(
        user_id: int,
        payload: UserUpdateEmailSchema,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_self_or_admin)
):
    """
    Update the email address of a user.
    """
    try:
        service = UserService(db)
        service.update_user_email(user_id, payload.new_email)
        return {"message": "User email updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}/password")
def update_user_password(
        user_id: int,
        payload: UserUpdatePasswordSchema,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_self_or_admin)
):
    """
    Update the password of a user.
    """
    try:
        service = UserService(db)
        service.update_user_password(user_id, payload.new_password)
        return {"message": "User password updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Delete a user by ID (admin only).
    """
    try:
        service = UserService(db)
        service.delete_user(user_id)
        return {"message": "User deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
