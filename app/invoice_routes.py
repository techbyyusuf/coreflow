from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from services.invoice_service import InvoiceService
from app.dependencies import get_db

router = APIRouter(prefix="/invoices", tags=["invoices"])


@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    """Retrieve all invoices"""
    try:
        service = InvoiceService(db)
        return service.get_all_invoices()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_invoice(
    customer_id: int,
    user_id: int,
    invoice_number: int,
    issue_date: date,
    due_date: date,
    status: str,
    referee: str,
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Create a new invoice"""
    try:
        service = InvoiceService(db)
        service.create_invoice(customer_id, user_id, invoice_number, issue_date, due_date, status, referee, notes)
        return {"message": "Invoice created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{invoice_id}/status")
def update_invoice_status(invoice_id: int, new_status: str, db: Session = Depends(get_db)):
    """Update invoice status"""
    try:
        service = InvoiceService(db)
        service.update_invoice_status(invoice_id, new_status)
        return {"message": "Invoice status updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Delete an invoice"""
    try:
        service = InvoiceService(db)
        service.delete_invoice(invoice_id)
        return {"message": "Invoice deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
