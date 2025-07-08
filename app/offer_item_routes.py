from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.offer_item_service import OfferItemService
from app.dependencies import get_db

router = APIRouter(prefix="/offer-items", tags=["offer items"])


@router.get("/")
def get_all_offer_items(db: Session = Depends(get_db)):
    """Retrieve all offer items"""
    try:
        service = OfferItemService(db)
        return service.get_all_offer_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_offer_item(
    offer_id: int,
    product_id: int,
    quantity: int,
    unit_price: float,
    db: Session = Depends(get_db)
):
    """Create a new offer item"""
    try:
        service = OfferItemService(db)
        service.create_offer_item(offer_id, product_id, quantity, unit_price)
        return {"message": "Offer item created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}/quantity")
def update_offer_item_quantity(item_id: int, new_quantity: int, db: Session = Depends(get_db)):
    """Update offer item quantity"""
    try:
        service = OfferItemService(db)
        service.update_offer_item_quantity(item_id, new_quantity)
        return {"message": "Offer item quantity updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
def delete_offer_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an offer item"""
    try:
        service = OfferItemService(db)
        service.delete_offer_item(item_id)
        return {"message": "Offer item deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
