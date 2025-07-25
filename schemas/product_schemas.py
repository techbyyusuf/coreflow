from pydantic import BaseModel, confloat
from typing import Optional

from models.enums import UnitType


class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """
    name: str
    unit_price: confloat(ge=0)
    unit: UnitType
    description: Optional[str] = None

class ProductUpdateName(BaseModel):
    """
    Schema for updating a product's name.
    """
    new_name: str

class ProductUpdatePrice(BaseModel):
    """
    Schema for updating a product's price.
    """
    new_price: float

class ProductUpdateUnit(BaseModel):
    """
    Schema for updating a product's unit.
    """
    new_unit: str

class ProductUpdateDescription(BaseModel):
    """
    Schema for updating a product's description.
    """
    new_description: str
