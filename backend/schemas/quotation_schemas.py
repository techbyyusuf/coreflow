from pydantic import BaseModel
from datetime import date
from typing import Optional, List

from schemas.quotation_item_schemas import QuotationItemResponseSchema

class QuotationCreateSchema(BaseModel):
    """
    Schema for creating a new quotation.
    """
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date] = None
    quotation_number: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None

class QuotationUpdateStatusSchema(BaseModel):
    """
    Schema for updating the status of a quotation.
    """
    new_status: str

class QuotationResponseSchema(BaseModel):
    """
    Schema for returning an order with its items.
    """
    id: int
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date]
    quotation_number: str
    status: str
    notes: Optional[str]
    items: List[QuotationItemResponseSchema]

    class Config:
        from_attributes = True