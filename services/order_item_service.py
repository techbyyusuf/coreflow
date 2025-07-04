import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.order_item import OrderItem

logger = logging.getLogger(__name__)


class OrderItemService:
    """
    Service class for handling CRUD operations related to OrderItem.
    """

    def __init__(self, session):
        """
        Initializes the OrderItemService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_order_item(self, order_id: int, product_id: int, quantity: int, unit_price: float) -> None:
        """
        Creates a new order item.

        :param order_id: ID of the order
        :param product_id: ID of the product
        :param quantity: Quantity of the product
        :param unit_price: Price per unit
        :raises SQLAlchemyError: If database error occurs
        """
        new_order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_order_item)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating order item for order {order_id}: {e}")
            raise

    def get_all_order_items(self):
        """
        Retrieves all order items.

        :return: List of OrderItem objects or empty list on error
        """
        try:
            return self.session.scalars(select(OrderItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving order items: {e}")
            return []

    def update_order_item_quantity(self, item_id: int, new_quantity: int) -> None:
        """
        Updates the quantity of an order item.

        :param item_id: ID of the order item
        :param new_quantity: New quantity value
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(OrderItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Order item with id '{item_id}' not found.")

            item.quantity = new_quantity
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating order item quantity: {e}")
            raise

    def delete_order_item(self, item_id: int) -> None:
        """
        Deletes an order item.

        :param item_id: ID of the order item
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(OrderItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Order item with id '{item_id}' does not exist.")

            self.session.delete(item)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order item with id '{item_id}': {e}")
            raise
