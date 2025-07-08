from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.customer_service import CustomerService
from app.dependencies import get_db

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
def get_all_customers(db: Session = Depends(get_db)):
    """Retrieve all customers"""
    try:
        service = CustomerService(db)
        return service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_customer(
    user_id: int,
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    address: str,
    tax_id: int,
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Create a new customer"""
    try:
        service = CustomerService(db)
        service.create_customer(user_id, first_name, last_name, email, phone, address, tax_id, notes)
        return {"message": "Customer created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}/email")
def update_customer_email(customer_id: int, new_email: str, db: Session = Depends(get_db)):
    """Update customer email"""
    try:
        service = CustomerService(db)
        service.update_customer_email(customer_id, new_email)
        return {"message": "Customer email updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}/phone")
def update_customer_phone(customer_id: int, new_phone: str, db: Session = Depends(get_db)):
    """Update customer phone"""
    try:
        service = CustomerService(db)
        service.update_customer_phone(customer_id, new_phone)
        return {"message": "Customer phone updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}/address")
def update_customer_address(customer_id: int, new_address: str, db: Session = Depends(get_db)):
    """Update customer address"""
    try:
        service = CustomerService(db)
        service.update_customer_address(customer_id, new_address)
        return {"message": "Customer address updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{customer_id}/notes")
def update_customer_notes(customer_id: int, new_notes: str, db: Session = Depends(get_db)):
    """Update customer notes"""
    try:
        service = CustomerService(db)
        service.update_customer_notes(customer_id, new_notes)
        return {"message": "Customer notes updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    try:
        service = CustomerService(db)
        service.delete_customer(customer_id)
        return {"message": "Customer deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
