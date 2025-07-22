from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.order_item_service import OrderItemService
from schemas.order_item_schemas import OrderItemCreateSchema, OrderItemUpdateSchema
from app.database.session import get_db
from security.dependencies import require_admin, require_employee

router = APIRouter(prefix="/order-items", tags=["order-items"])


@router.get("/")
def get_all_order_items(
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Retrieve all order items"""
    service = OrderItemService(db)
    try:
        return service.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_order_item(
        payload: OrderItemCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Create a new order item"""
    service = OrderItemService(db)
    try:
        service.create_item(
            order_id=payload.order_id,
            product_id=payload.product_id,
            quantity=payload.quantity,
            unit_price=payload.unit_price
        )
        return {"message": "Order item created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{item_id}")
def update_order_item(item_id: int,
                      payload: OrderItemUpdateSchema,
                      db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """Update an order item"""
    service = OrderItemService(db)
    try:
        service.update_item(item_id, payload.new_quantity, payload.new_unit_price)
        return {"message": "Order item updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{item_id}")
def delete_order_item(item_id: int,
                      db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """Delete an order item"""
    service = OrderItemService(db)
    try:
        service.delete_item(item_id)
        return {"message": "Order item deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
