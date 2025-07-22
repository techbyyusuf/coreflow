from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceCreateSchema(BaseModel):
    """
    Schema for creating a new invoice.
    """
    customer_id: int
    user_id: int
    issue_date: date
    due_date: Optional[date] = None
    invoice_number: Optional[str] = None
    status: str = "DRAFT"
    notes: Optional[str] = None

class InvoiceUpdateStatusSchema(BaseModel):
    """
    Schema for updating the status of an invoice.
    """
    new_status: str
