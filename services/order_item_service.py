from models.order_item import OrderItem
from models.order import Order
from services.base_item_services import BaseItemService

class OrderItemService(BaseItemService):
    def __init__(self, session):
        super().__init__(session, OrderItem, Order)
