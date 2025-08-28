from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from services.quotation_service import QuotationService
from schemas.quotation_schemas import QuotationCreateSchema, QuotationUpdateStatusSchema, QuotationResponseSchema
from app.database.session import get_db
from security.dependencies import require_admin, require_viewer, require_employee

router = APIRouter(prefix="/quotations", tags=["quotations"])


@router.get("/")
def get_all_quotations(
        status: Optional[str] = Query(None),
        customer_id: Optional[int] = Query(None),
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve all quotations or filter by status.
    """
    service = QuotationService(db)
    try:
        return service.get_all_quotations(status, customer_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_quotation(
        payload: QuotationCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Create a new quotation.
    """
    service = QuotationService(db)
    try:
        service.create_quotation(
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
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
def update_quotation_status(
        quotation_id: int,
        payload: QuotationUpdateStatusSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update the status of a quotation.
    """
    service = QuotationService(db)
    try:
        service.update_quotation_status(quotation_id, payload.new_status)
        return {"message": "Quotation status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{quotation_id}")
def delete_quotation(
        quotation_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Delete a quotation by ID.
    """
    service = QuotationService(db)
    try:
        service.delete_quotation(quotation_id)
        return {"message": "Quotation deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{quotation_id}", response_model=QuotationResponseSchema)
def get_quotation_by_id(
        quotation_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve a specific quotation including its items.
    """
    service = QuotationService(db)
    try:
        quotation = service.get_quotation_by_id_or_raise(quotation_id)
        return quotation
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))