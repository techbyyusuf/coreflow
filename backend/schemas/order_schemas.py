from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from schemas.order_item_schemas import OrderItemResponseSchema

class OrderCreateSchema(BaseModel):
    """
    Schema for creating a new order.
    """
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date] = None
    delivery_date : Optional[date] = None
    order_number: Optional[str] = None
    status: str = "draft"
    reference: Optional[str] = None
    notes: Optional[str] = None

class OrderUpdateStatusSchema(BaseModel):
    """
    Schema for updating the status of an order.
    """
    new_status: str

class OrderResponseSchema(BaseModel):
    """
    Schema for returning an order with its items.
    """
    id: int
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date]
    delivery_date: Optional[date]
    order_number: str
    status: str
    reference: Optional[str]
    notes: Optional[str]
    items: List[OrderItemResponseSchema]

    class Config:
        from_attributes = True