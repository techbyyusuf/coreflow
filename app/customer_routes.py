from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.customer_service import CustomerService
from security.dependencies import require_admin, require_viewer, require_employee
from app.database.session import get_db
from schemas.customer_schemas import (
    CustomerCreateSchema,
    CustomerUpdateEmailSchema,
    CustomerUpdatePhoneSchema,
    CustomerUpdateAddressSchema,
    CustomerUpdateNotesSchema
)

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/")
def get_all_customers(
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve all customers from the database.
    """
    try:
        service = CustomerService(db)
        return service.get_all_customers()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_customer(
        payload: CustomerCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Create a new customer with optional fields.
    """
    try:
        service = CustomerService(db)
        service.create_customer(
            payload.name,
            payload.company_name,
            payload.email,
            payload.phone,
            payload.address,
            payload.tax_id,
            payload.notes
        )
        return {"message": "Customer created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{customer_id}/email")
def update_customer_email(
        customer_id: int,
        payload: CustomerUpdateEmailSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update a customer's email address.
    """
    try:
        service = CustomerService(db)
        service.update_customer_email(customer_id, payload.new_email)
        return {"message": "Customer email updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{customer_id}/phone")
def update_customer_phone(
        customer_id: int,
        payload: CustomerUpdatePhoneSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update a customer's phone number.
    """
    try:
        service = CustomerService(db)
        service.update_customer_phone(customer_id, payload.new_phone)
        return {"message": "Customer phone updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{customer_id}/address")
def update_customer_address(
        customer_id: int,
        payload: CustomerUpdateAddressSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update a customer's address.
    """
    try:
        service = CustomerService(db)
        service.update_customer_address(customer_id, payload.new_address)
        return {"message": "Customer address updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{customer_id}/notes")
def update_customer_notes(
        customer_id: int,
        payload: CustomerUpdateNotesSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update a customer's notes field.
    """
    try:
        service = CustomerService(db)
        service.update_customer_notes(customer_id, payload.new_notes)
        return {"message": "Customer notes updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{customer_id}")
def delete_customer(
        customer_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Delete a customer by ID.
    """
    try:
        service = CustomerService(db)
        service.delete_customer(customer_id)
        return {"message": "Customer deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
