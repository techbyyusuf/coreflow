from pydantic import BaseModel, confloat

class InvoiceItemCreateSchema(BaseModel):
    """
    Schema for creating an invoice item.
    """
    invoice_id: int
    product_id: int
    quantity: confloat(ge=0)
    unit_price: confloat(ge=0)

class InvoiceItemUpdateSchema(BaseModel):
    """
    Schema for updating an invoice item.
    """
    new_quantity: confloat(ge=0)
    new_unit_price: confloat(ge=0)
