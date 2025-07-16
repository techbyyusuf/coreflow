from pydantic import BaseModel, confloat
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    unit_price: confloat(ge=0)
    unit: str
    description: Optional[str] = None

class ProductUpdateName(BaseModel):
    new_name: str

class ProductUpdatePrice(BaseModel):
    new_price: float

class ProductUpdateUnit(BaseModel):
    new_unit: str

class ProductUpdateDescription(BaseModel):
    new_description: str
