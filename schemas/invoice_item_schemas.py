from pydantic import BaseModel, confloat

class InvoiceItemCreateSchema(BaseModel):
    invoice_id: int
    product_id: int
    quantity: confloat(ge=0)
    unit_price: confloat(ge=0)

class InvoiceItemUpdateSchema(BaseModel):
    new_quantity: confloat(ge=0)
    new_unit_price: confloat(ge=0)
