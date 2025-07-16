from pydantic import BaseModel


class QuotationItemCreateSchema(BaseModel):
    quotation_id: int
    product_id: int
    quantity: float
    unit_price: float


class QuotationItemUpdateSchema(BaseModel):
    new_quantity: float
    new_unit_price: float
