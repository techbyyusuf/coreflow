from pydantic import BaseModel, confloat

class QuotationItemCreateSchema(BaseModel):
    """
    Schema for creating a quotation item.
    """
    quotation_id: int
    product_id: int
    quantity: confloat(ge=0)
    unit_price: confloat(ge=0)

class QuotationItemUpdateSchema(BaseModel):
    """
    Schema for updating a quotation item.
    """
    new_quantity: confloat(ge=0)
    new_unit_price: confloat(ge=0)

class QuotationItemResponseSchema(BaseModel):
    """
    Schema for returning quotation item data.
    """
    id: int
    product_id: int
    quantity: float
    unit_price: float

    class Config:
        orm_mode = True