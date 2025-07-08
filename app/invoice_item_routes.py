from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.invoice_item_service import InvoiceItemService
from app.dependencies import get_db

router = APIRouter(prefix="/invoice-items", tags=["invoice items"])


@router.get("/")
def get_all_invoice_items(db: Session = Depends(get_db)):
    """Retrieve all invoice items"""
    try:
        service = InvoiceItemService(db)
        return service.get_all_invoice_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_invoice_item(
    invoice_id: int,
    product_id: int,
    quantity: int,
    unit_price: float,
    db: Session = Depends(get_db)
):
    """Create a new invoice item"""
    try:
        service = InvoiceItemService(db)
        service.create_invoice_item(invoice_id, product_id, quantity, unit_price)
        return {"message": "Invoice item created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}/quantity")
def update_invoice_item_quantity(item_id: int, new_quantity: int, db: Session = Depends(get_db)):
    """Update invoice item quantity"""
    try:
        service = InvoiceItemService(db)
        service.update_invoice_item_quantity(item_id, new_quantity)
        return {"message": "Invoice item quantity updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
def delete_invoice_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an invoice item"""
    try:
        service = InvoiceItemService(db)
        service.delete_invoice_item(item_id)
        return {"message": "Invoice item deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
