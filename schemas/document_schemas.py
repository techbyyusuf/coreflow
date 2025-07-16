from pydantic import BaseModel
from typing import Optional
from datetime import date

class DocumentCreateSchema(BaseModel):
    document_type: str
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date] = None
    delivery_date: Optional[date] = None
    invoice_number: Optional[str] = None
    status: str = "OPEN"
    reference: Optional[str] = None
    notes: Optional[str] = None

class DocumentUpdateStatusSchema(BaseModel):
    new_status: str
