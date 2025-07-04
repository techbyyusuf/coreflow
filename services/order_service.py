import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from models.order import Order


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderService:
    """
    Service class for handling CRUD operations related to Order.
    """

    def __init__(self, session):
        """
        Initializes the OrderService with a database session.
        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_order(self, customer_id: int, user_id: int, issue_date: date, delivery_date: date, status: str, notes: str = None) -> None:
        """
        Creates a new order in the database.
        :param customer_id: ID of the customer
        :param user_id: ID of the user creating the order
        :param issue_date: Issue date of the order
        :param delivery_date: Delivery date of the order
        :param status: Status of the order
        :param notes: Optional notes
        :raises SQLAlchemyError: If database error occurs
        """
        new_order = Order(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            delivery_date=delivery_date,
            status=status,
            notes=notes
        )

        try:
            self.session.add(new_order)
            self.session.commit()
            logger.info(f"Order for customer {customer_id} created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating order: {e}")
            raise

    def get_all_orders(self):
        """
        Retrieves all orders from the database.
        :return: List of Order objects or empty list on error
        """
        try:
            return self.session.scalars(select(Order)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving orders: {e}")
            return []

    def update_order_status(self, order_id: int, new_status: str) -> None:
        """
        Updates the status of an order.
        :param order_id: ID of the order to update
        :param new_status: New status
        :raises ValueError: If order not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            order = self.session.scalars(select(Order)).filter_by(id=order_id).first()
            if not order:
                raise ValueError(f"Order with id {order_id} not found.")

            order.status = new_status
            self.session.commit()
            logger.info(f"Order status updated successfully for id {order_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating order status: {e}")
            raise

    def update_order_delivery_date(self, order_id: int, new_delivery_date: date) -> None:
        """
        Updates the delivery date of an order.
        :param order_id: ID of the order to update
        :param new_delivery_date: New delivery date
        :raises ValueError: If order not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            order = self.session.scalars(select(Order)).filter_by(id=order_id).first()
            if not order:
                raise ValueError(f"Order with id {order_id} not found.")

            order.delivery_date = new_delivery_date
            self.session.commit()
            logger.info(f"Order delivery date updated successfully for id {order_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating delivery date: {e}")
            raise

    def update_order_notes(self, order_id: int, new_notes: str) -> None:
        """
        Updates the notes of an order.
        :param order_id: ID of the order to update
        :param new_notes: New notes
        :raises ValueError: If order not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            order = self.session.scalars(select(Order)).filter_by(id=order_id).first()
            if not order:
                raise ValueError(f"Order with id {order_id} not found.")

            order.notes = new_notes
            self.session.commit()
            logger.info(f"Order notes updated successfully for id {order_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating order notes: {e}")
            raise

    def delete_order(self, order_id: int) -> None:
        """
        Deletes an order from the database.
        :param order_id: ID of the order to delete
        :raises ValueError: If order not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            order = self.session.scalars(select(Order)).filter_by(id=order_id).first()
            if not order:
                raise ValueError(f"Order with id '{order_id}' does not exist.")

            self.session.delete(order)
            self.session.commit()
            logger.info(f"Order with id '{order_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order with id '{order_id}': {e}")
            raise
