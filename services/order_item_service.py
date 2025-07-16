import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.order_item import OrderItem
from models.order import Order

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderItemService:
    def __init__(self, session):
        self.session = session


    def get_order_by_id(self, order_id: int):
        stmt = select(Order).where(Order.id == order_id)
        order = self.session.scalars(stmt).first()
        if not order:
            raise ValueError(f"Order with id '{order_id}' not found.")
        return order


    def get_item_by_id(self, item_id: int):
        stmt = select(OrderItem).where(OrderItem.id == item_id)
        item = self.session.scalars(stmt).first()
        if not item:
            raise ValueError(f"Item with id '{item_id}' does not exist.")
        return item


    def create_item(self, order_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")

        new_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_item)
            self.session.commit()
            logger.info(f"Item created successfully for order id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating order item: {e}")
            raise


    def update_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        item = self.get_item_by_id(item_id)

        try:
            item.quantity = new_quantity
            item.unit_price = new_unit_price
            self.session.commit()
            logger.info(f"Order item updated successfully for id {item_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order item: {e}")
            raise


    def delete_item(self, item_id: int) -> None:
        item = self.get_item_by_id(item_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Order item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order item with id '{item_id}': {e}")
            raise


    def get_all_items(self):
        try:
            return self.session.scalars(select(OrderItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving order items: {e}")
            return []
