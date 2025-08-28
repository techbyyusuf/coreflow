from pydantic import BaseModel, model_validator
from typing import Optional

class CustomerCreateSchema(BaseModel):
    """
    Schema for creating a new customer.
    """
    name: Optional[str] = None
    company_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    notes: Optional[str] = None

    @model_validator(mode="after")
    def check_name_or_company(self) -> "CustomerCreateSchema":
        if not self.name and not self.company_name:
            raise ValueError(
                "At least one of 'name' or 'company_name' must be provided.")
        return self

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
