from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreateSchema(BaseModel):
    """
    Schema for creating a new customer.
    """
    name: Optional[str] = None
    company_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    notes: Optional[str] = None

class CustomerUpdateEmailSchema(BaseModel):
    """
    Schema for updating a customer's email.
    """
    new_email: str

class CustomerUpdatePhoneSchema(BaseModel):
    """
    Schema for updating a customer's phone number.
    """
    new_phone: str

class CustomerUpdateAddressSchema(BaseModel):
    """
    Schema for updating a customer's address.
    """
    new_address: str

class CustomerUpdateNotesSchema(BaseModel):
    """
    Schema for updating a customer's notes field.
    """
    new_notes: str
