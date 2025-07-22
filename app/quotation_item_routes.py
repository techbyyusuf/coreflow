from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.quotation_item_service import QuotationItemService
from schemas.quotation_item_schemas import QuotationItemCreateSchema, QuotationItemUpdateSchema
from app.database.session import get_db
from security.dependencies import require_admin, require_employee

router = APIRouter(prefix="/quotation-items", tags=["quotation_items"])


@router.get("/")
def get_all_quotation_items(
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Retrieve all quotation items"""
    service = QuotationItemService(db)
    try:
        return service.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_quotation_item(
        payload: QuotationItemCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Create a new quotation item"""
    service = QuotationItemService(db)
    try:
        service.create_item(
            quotation_id=payload.quotation_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price
        )
        return {"message": "Quotation item created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
def update_quotation_item(
        item_id: int,
        payload: QuotationItemUpdateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Update a quotation item"""
    service = QuotationItemService(db)
    try:
        service.update_item(item_id, payload.new_quantity, payload.new_unit_price)
        return {"message": "Quotation item updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
def delete_quotation_item(item_id: int,
                          db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """Delete a quotation item"""
    service = QuotationItemService(db)
    try:
        service.delete_item(item_id)
        return {"message": "Quotation item deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
