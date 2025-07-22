from pydantic import BaseModel
from datetime import date
from typing import Optional

class QuotationCreateSchema(BaseModel):
    """
    Schema for creating a new quotation.
    """
    customer_id: int
    user_id: int
    issue_date: date
    quotation_number: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None

class QuotationUpdateStatusSchema(BaseModel):
    """
    Schema for updating the status of a quotation.
    """
    new_status: str
