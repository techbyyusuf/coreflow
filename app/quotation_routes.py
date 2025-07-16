from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from services.quotation_service import QuotationService
from schemas.quotation_schemas import QuotationCreateSchema, QuotationUpdateStatusSchema
from app.dependencies import get_db

router = APIRouter(prefix="/quotations", tags=["quotations"])


@router.get("/")
def get_all_quotations(status: str = Query(None), db: Session = Depends(get_db)):
    """Retrieve all quotations, optionally filtered by status"""
    service = QuotationService(db)
    try:
        if status:
            return service.get_quotations_by_status(status)
        else:
            return service.get_all_quotations()
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_quotation(payload: QuotationCreateSchema, db: Session = Depends(get_db)):
    """Create a new quotation"""
    service = QuotationService(db)
    try:
        service.create_quotation(
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            quotation_number=payload.quotation_number,
            status=payload.status,
            notes=payload.notes
        )
        return {"message": "Quotation created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{quotation_id}/status")
def update_quotation_status(quotation_id: int, payload: QuotationUpdateStatusSchema, db: Session = Depends(get_db)):
    """Update quotation status"""
    service = QuotationService(db)
    try:
        service.update_quotation_status(quotation_id, payload.new_status)
        return {"message": "Quotation status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{quotation_id}")
def delete_quotation(quotation_id: int, db: Session = Depends(get_db)):
    """Delete a quotation"""
    service = QuotationService(db)
    try:
        service.delete_quotation(quotation_id)
        return {"message": "Quotation deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
