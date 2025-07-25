from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from services.invoice_service import InvoiceService
from schemas.invoice_schemas import InvoiceCreateSchema, InvoiceUpdateStatusSchema, InvoiceResponseSchema
from app.database.session import get_db
from security.dependencies import require_admin, require_viewer, require_employee

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/")
def get_all_invoices(
        status: Optional[str] = Query(None),
        invoice_number: Optional[str] = Query(None),
        customer_id: Optional[int] = Query(None),
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve all invoices or filter by status, invoice number or customer ID.
    """
    service = InvoiceService(db)
    try:
        return service.get_all_invoices(
            status=status,
            invoice_number=invoice_number,
            customer_id=customer_id
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_invoice(
        payload: InvoiceCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Create a new invoice with optional due date, number, and notes.
    """
    service = InvoiceService(db)
    try:
        service.create_invoice(
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
            invoice_number=payload.invoice_number,
            status=payload.status,
            notes=payload.notes,
        )
        return {"message": "Invoice created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{invoice_id}/status")
def update_invoice_status(
        invoice_id: int,
        payload: InvoiceUpdateStatusSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update the status of an invoice by ID.
    """
    service = InvoiceService(db)
    try:
        service.update_invoice_status(invoice_id, payload.new_status)
        return {"message": "Invoice status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{invoice_id}")
def delete_invoice(
        invoice_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Delete an invoice by ID.
    """
    service = InvoiceService(db)
    try:
        service.delete_invoice(invoice_id)
        return {"message": "Invoice deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{invoice_id}", response_model=InvoiceResponseSchema)
def get_invoice_by_id(
        invoice_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve a specific invoice including its items.
    """
    service = InvoiceService(db)
    try:
        invoice = service.get_invoice_by_id_or_raise(invoice_id)
        return invoice
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))