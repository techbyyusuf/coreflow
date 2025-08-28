import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.order_item import OrderItem
from models.order import Order
from models.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderItemService:
    """
    Service class for managing order items, including creation, updates, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_order_by_id_or_raise(self, order_id: int):
        """
        Retrieves an order by ID or raises an error if not found.

        Args:
            order_id (int): ID of the order.

        Returns:
            Order: The found order.
        """
        stmt = select(Order).where(Order.id == order_id)
        order = self.session.scalars(stmt).first()
        if not order:
            raise ValueError(f"Order with id '{order_id}' not found.")
        return order


    def get_product_by_id_or_raise(self, product_id: int):
        """
        Retrieves a product by ID or raises an error if not found.

        Args:
            product_id (int): ID of the product.

        Returns:
            Product: The found product.
        """
        stmt = select(Product).where(Product.id == product_id)
        product = self.session.scalars(stmt).first()
        if not product:
            raise ValueError(f"Product with id '{product_id}' not found.")
        return product


    def get_item_by_id_or_raise(self, item_id: int):
        """
        Retrieves an order item by ID or raises an error if not found.

        Args:
            item_id (int): ID of the order item.

        Returns:
            OrderItem: The found item.
        """
        stmt = select(OrderItem).where(OrderItem.id == item_id)
        item = self.session.scalars(stmt).first()
        if not item:
            raise ValueError(f"Item with id '{item_id}' does not exist.")
        return item


    def get_all_items(self):
        """
        Retrieves all order items from the database.

        Returns:
            list: List of OrderItem objects.
        """
        try:
            return self.session.scalars(select(OrderItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving order items: {e}")
            return []


    def create_item(self, order_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        """
        Creates a new order item after checking related entities and input values.

        Args:
            order_id (int): ID of the order.
            product_id (int): ID of the product.
            quantity (float): Quantity ordered.
            unit_price (float): Unit price of the product.

        Raises:
            ValueError: If inputs are invalid.
        """
        self.get_order_by_id_or_raise(order_id)
        self.get_product_by_id_or_raise(product_id)

        if quantity < 0:
            raise ValueError("Quantity must be zero or positive.")
        if unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

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
        """
        Updates quantity and unit price of an existing order item.

        Args:
            item_id (int): ID of the item to update.
            new_quantity (float): New quantity value.
            new_unit_price (float): New price value.

        Raises:
            ValueError: If inputs are invalid.
        """
        item = self.get_item_by_id_or_raise(item_id)

        if new_quantity < 0:
            raise ValueError("Quantity must be zero or positive.")
        if new_unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

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
        """
        Deletes an order item by ID.

        Args:
            item_id (int): ID of the item to delete.
        """
        item = self.get_item_by_id_or_raise(item_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Order item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order item with id '{item_id}': {e}")
            raise
