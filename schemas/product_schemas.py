from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    unit_price: float
    unit: str
    description: str | None = None

class ProductUpdateName(BaseModel):
    new_name: str

class ProductUpdatePrice(BaseModel):
    new_price: float

class ProductUpdateUnit(BaseModel):
    new_unit: str

class ProductUpdateDescription(BaseModel):
    new_description: str
