from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.invoice_item_service import InvoiceItemService
from schemas.invoice_item_schemas import InvoiceItemCreateSchema, InvoiceItemUpdateSchema
from app.database.session import get_db
from security.dependencies import require_admin, require_employee

router = APIRouter(prefix="/invoice-items", tags=["invoice_items"])


@router.get("/")
def get_all_invoice_items(
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Retrieve all invoice items"""
    service = InvoiceItemService(db)
    try:
        return service.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_invoice_item(
        payload: InvoiceItemCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Create a new invoice item"""
    service = InvoiceItemService(db)
    try:
        service.create_item(
            invoice_id=payload.invoice_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price
        )
        return {"message": "Invoice item created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
def update_invoice_item(
        item_id: int,
        payload: InvoiceItemUpdateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Update an invoice item"""
    service = InvoiceItemService(db)
    try:
        service.update_item(item_id, payload.new_quantity, payload.new_unit_price)
        return {"message": "Invoice item updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
def delete_invoice_item(
        item_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """Delete an invoice item"""
    service = InvoiceItemService(db)
    try:
        service.delete_item(item_id)
        return {"message": "Invoice item deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
