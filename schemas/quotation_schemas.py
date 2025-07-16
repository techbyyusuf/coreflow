from pydantic import BaseModel
from datetime import date

class QuotationCreateSchema(BaseModel):
    customer_id: int
    user_id: int
    issue_date: date
    quotation_number: str | None = None
    status: str
    notes: str | None = None

class QuotationUpdateStatusSchema(BaseModel):
    new_status: str
