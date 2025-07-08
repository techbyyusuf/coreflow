from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.order_item_service import OrderItemService
from app.dependencies import get_db

router = APIRouter(prefix="/order-items", tags=["order items"])


@router.get("/")
def get_all_order_items(db: Session = Depends(get_db)):
    """Retrieve all order items"""
    try:
        service = OrderItemService(db)
        return service.get_all_order_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_order_item(
    order_id: int,
    product_id: int,
    quantity: int,
    unit_price: float,
    db: Session = Depends(get_db)
):
    """Create a new order item"""
    try:
        service = OrderItemService(db)
        service.create_order_item(order_id, product_id, quantity, unit_price)
        return {"message": "Order item created successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}/quantity")
def update_order_item_quantity(item_id: int, new_quantity: int, db: Session = Depends(get_db)):
    """Update order item quantity"""
    try:
        service = OrderItemService(db)
        service.update_order_item_quantity(item_id, new_quantity)
        return {"message": "Order item quantity updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an order item"""
    try:
        service = OrderItemService(db)
        service.delete_order_item(item_id)
        return {"message": "Order item deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
