from pydantic import BaseModel

class OrderItemCreateSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: float
    unit_price: float

class OrderItemUpdateSchema(BaseModel):
    new_quantity: float
    new_unit_price: float
