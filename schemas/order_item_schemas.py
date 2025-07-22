from pydantic import BaseModel, confloat

class OrderItemCreateSchema(BaseModel):
    """
    Schema for creating an order item.
    """
    order_id: int
    product_id: int
    quantity: confloat(ge=0)
    unit_price: confloat(ge=0)

class OrderItemUpdateSchema(BaseModel):
    """
    Schema for updating an order item.
    """
    new_quantity: confloat(ge=0)
    new_unit_price: confloat(ge=0)
