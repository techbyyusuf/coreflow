from pydantic import BaseModel, confloat

class OrderItemCreateSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: confloat(ge=0)
    unit_price: confloat(ge=0)

class OrderItemUpdateSchema(BaseModel):
    new_quantity: confloat(ge=0)
    new_unit_price: confloat(ge=0)
