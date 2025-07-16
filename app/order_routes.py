from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.order_service import OrderService
from schemas.order_schemas import OrderCreateSchema, OrderUpdateStatusSchema
from app.dependencies import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/")
def get_all_orders(status: str = None, db: Session = Depends(get_db)):
    """Retrieve all orders, optionally filtered by status"""
    service = OrderService(db)
    try:
        if status:
            return service.get_orders_by_status(status)
        return service.get_all_orders()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")
def create_order(payload: OrderCreateSchema, db: Session = Depends(get_db)):
    """Create a new order"""
    service = OrderService(db)
    try:
        service.create_order(
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
            order_number=payload.order_number,
            status=payload.status,
            notes=payload.notes
        )
        return {"message": "Order created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{order_id}/status")
def update_order_status(order_id: int, payload: OrderUpdateStatusSchema, db: Session = Depends(get_db)):
    """Update order status"""
    service = OrderService(db)
    try:
        service.update_order_status(order_id, payload.new_status)
        return {"message": "Order status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    service = OrderService(db)
    try:
        service.delete_order(order_id)
        return {"message": "Order deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


