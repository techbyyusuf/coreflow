from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from services.order_service import OrderService
from schemas.order_schemas import OrderCreateSchema, OrderUpdateStatusSchema, OrderResponseSchema
from app.database.session import get_db
from security.dependencies import require_employee, require_viewer, require_admin

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
def get_all_orders(
        status: Optional[str] = Query(None),
        order_number: Optional[str] = Query(None),
        customer_id: Optional[str] = Query(None),
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve all orders, optionally filtered by status, order number or customer ID.
    """
    service = OrderService(db)
    try:
        orders = service.get_all_orders(
            status=status,
            order_number=order_number,
            customer_id=customer_id
        )
        return orders
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
def create_order(
        payload: OrderCreateSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Create a new order.
    """
    service = OrderService(db)
    try:
        service.create_order(
            customer_id=payload.customer_id,
            user_id=payload.user_id,
            issue_date=payload.issue_date,
            due_date=payload.due_date,
            delivery_date=payload.delivery_date,
            order_number=payload.order_number,
            status=payload.status,
            reference=payload.reference,
            notes=payload.notes
        )
        return {"message": "Order created successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{order_id}/status")
def update_order_status(
        order_id: int,
        payload: OrderUpdateStatusSchema,
        db: Session = Depends(get_db),
        user = Depends(require_employee)
):
    """
    Update the status of an order.
    """
    service = OrderService(db)
    try:
        service.update_order_status(order_id, payload.new_status)
        return {"message": "Order status updated successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{order_id}")
def delete_order(
        order_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_admin)
):
    """
    Delete an order by ID.
    """
    service = OrderService(db)
    try:
        service.delete_order(order_id)
        return {"message": "Order deleted successfully."}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{order_id}", response_model=OrderResponseSchema)
def get_order_by_id(
        order_id: int,
        db: Session = Depends(get_db),
        user = Depends(require_viewer)
):
    """
    Retrieve a specific order including its items.
    """
    service = OrderService(db)
    try:
        order = service.get_order_by_id_or_raise(order_id)
        return order
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))