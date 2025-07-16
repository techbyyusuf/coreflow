from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreateSchema(BaseModel):
    name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    notes: Optional[str] = None

class CustomerUpdateEmailSchema(BaseModel):
    new_email: str

class CustomerUpdatePhoneSchema(BaseModel):
    new_phone: str

class CustomerUpdateAddressSchema(BaseModel):
    new_address: str

class CustomerUpdateNotesSchema(BaseModel):
    new_notes: str
