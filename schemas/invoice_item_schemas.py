from pydantic import BaseModel

class InvoiceItemCreateSchema(BaseModel):
    invoice_id: int
    product_id: int
    quantity: float
    unit_price: float

class InvoiceItemUpdateSchema(BaseModel):
    new_quantity: float
    new_unit_price: float
