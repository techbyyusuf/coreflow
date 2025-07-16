from pydantic import BaseModel
from datetime import date
from typing import Optional

class OrderCreateSchema(BaseModel):
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date] = None
    invoice_number: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None

class OrderUpdateStatusSchema(BaseModel):
    new_status: str
