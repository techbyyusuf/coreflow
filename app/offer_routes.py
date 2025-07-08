from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from services.offer_service import OfferService
from app.dependencies import get_db

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get("/")
def get_all_offers(db: Session = Depends(get_db)):
    """Retrieve all offers"""
    try:
        service = OfferService(db)
        return service.get_all_offers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_offer(
    customer_id: int,
    user_id: int,
    issue_date: date,
    valid_until: date,
    status: str,
    notes: str = None,
    db: Session = Depends(get_db)
):
    """Create a new offer"""
    try:
        service = OfferService(db)
        service.create_offer(customer_id, user_id, issue_date, valid_until, status, notes)
        return {"message": "Offer created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{offer_id}/status")
def update_offer_status(offer_id: int, new_status: str, db: Session = Depends(get_db)):
    """Update offer status"""
    try:
        service = OfferService(db)
        service.update_offer_status(offer_id, new_status)
        return {"message": "Offer status updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    """Delete an offer"""
    try:
        service = OfferService(db)
        service.delete_offer(offer_id)
        return {"message": "Offer deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
