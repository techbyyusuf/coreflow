from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from services.order_service import OrderService
from app.dependencies import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    try:
        service = OrderService(db)
        return service.get_all_orders()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_order(
    customer_id: int,
    user_id: int,
    issue_date: date,
    delivery_date: date,
    status: str,
    notes: str = None,
    db: Session = Depends(get_db)
):
    try:
        service = OrderService(db)
        service.create_order(customer_id, user_id, issue_date, delivery_date, status, notes)
        return {"message": "Order created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}/status")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):
    try:
        service = OrderService(db)
        service.update_order_status(order_id, new_status)
        return {"message": "Order status updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}/delivery-date")
def update_order_delivery_date(order_id: int, new_delivery_date: date, db: Session = Depends(get_db)):
    try:
        service = OrderService(db)
        service.update_order_delivery_date(order_id, new_delivery_date)
        return {"message": "Order delivery date updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}/notes")
def update_order_notes(order_id: int, new_notes: str, db: Session = Depends(get_db)):
    try:
        service = OrderService(db)
        service.update_order_notes(order_id, new_notes)
        return {"message": "Order notes updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        service = OrderService(db)
        service.delete_order(order_id)
        return {"message": "Order deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
