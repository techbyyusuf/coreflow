from pydantic import BaseModel
from datetime import date
from typing import Optional

class QuotationCreateSchema(BaseModel):
    customer_id: int
    user_id: int
    issue_date: date
    quotation_number: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None

class QuotationUpdateStatusSchema(BaseModel):
    new_status: str
