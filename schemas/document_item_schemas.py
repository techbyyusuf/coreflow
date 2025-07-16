from pydantic import BaseModel

class DocumentItemCreateSchema(BaseModel):
    document_id: int
    product_id: int
    quantity: float
    unit_price: float

class DocumentItemUpdateSchema(BaseModel):
    new_quantity: float
    new_unit_price: float
