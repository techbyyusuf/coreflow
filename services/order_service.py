import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.order import Order
from models.enums import OrderStatus
from models.customer import Customer
from models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderService:
    """
    Service class for managing customer orders, including creation, updates, retrieval, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_order_by_id_or_raise(self, order_id: int) -> Order | None:
        """
        Retrieves an order by ID or raises an error if not found.

        Args:
            order_id (int): ID of the order.

        Returns:
            Order: The order instance.
        """
        stmt = select(Order).where(Order.id == order_id)
        order = self.session.scalars(stmt).first()
        if not order:
            raise ValueError(f"Order with id '{order_id}' not found.")
        return order


    def get_customer_or_raise(self, customer_id: int) -> Customer:
        """
        Retrieves a customer by ID or raises an error if not found.

        Args:
            customer_id (int): ID of the customer.

        Returns:
            Customer: The customer instance.
        """
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = self.session.scalars(stmt).first()

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")
        return customer


    def get_user_or_raise(self, user_id: int) -> User:
        """
        Retrieves a user by ID or raises an error if not found.

        Args:
            user_id (int): ID of the user.

        Returns:
            User: The user instance.
        """
        stmt = select(User).where(User.id == user_id)
        user = self.session.scalars(stmt).first()

        if not user:
            raise ValueError(f"User with id {user_id} not found.")
        return user


    def create_order(
        self,
        customer_id: int,
        user_id: int,
        issue_date,
        due_date=None,
        delivery_date=None,
        order_number=None,
        status: str = "DRAFT",
        reference: str = None,
        notes: str = None
    ) -> None:
        """
        Creates a new order with optional fields and validations.

        Args:
            customer_id (int): ID of the customer.
            user_id (int): ID of the user.
            issue_date (date): Date the order was issued.
            due_date (date, optional): Due date.
            delivery_date (date, optional): Delivery date.
            order_number (str, optional): Unique order number.
            status (str): Status string, must match OrderStatus enum.
            reference (str, optional): Reference text.
            notes (str, optional): Notes for the order.

        Raises:
            ValueError: If validation fails.
        """
        self.get_user_or_raise(user_id)
        self.get_customer_or_raise(customer_id)

        if order_number is not None:
            stmt = select(Order).where(Order.order_number == order_number)
            existing_order = self.session.scalars(stmt).first()
            if existing_order:
                raise ValueError("Order number already in use.")

        if status.upper() not in OrderStatus.__members__:
            raise ValueError(f"Invalid order status: {status}")

        new_order = Order(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date,
            delivery_date=delivery_date,
            order_number=order_number,
            status=OrderStatus[status.upper()],
            reference=reference,
            notes=notes
        )

        try:
            self.session.add(new_order)
            self.session.commit()
            logger.info(f"Order created successfully for customer id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating order: {e}")
            raise


    def get_all_orders(self):
        """
        Retrieves all orders from the database.

        Returns:
            list: List of Order instances.
        """
        try:
            return self.session.scalars(select(Order)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving orders: {e}")
            return []


    def update_order_status(self, order_id: int, new_status: str) -> None:
        """
        Updates the status of an order.

        Args:
            order_id (int): ID of the order.
            new_status (str): New status value.

        Raises:
            ValueError: If new status is invalid.
        """
        order = self.get_order_by_id_or_raise(order_id)

        if new_status.upper() not in OrderStatus.__members__:
            raise ValueError(f"Invalid order status: {new_status}")

        try:
            order.status = OrderStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Order status updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order status: {e}")
            raise


    def update_order_reference(self, order_id: int, new_reference: str) -> None:
        """
        Updates the reference field of an order.

        Args:
            order_id (int): ID of the order.
            new_reference (str): New reference text.
        """
        order = self.get_order_by_id_or_raise(order_id)

        try:
            order.reference = new_reference
            self.session.commit()
            logger.info(f"Order reference updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order reference: {e}")
            raise


    def update_order_notes(self, order_id: int, new_notes: str) -> None:
        """
        Updates the notes field of an order.

        Args:
            order_id (int): ID of the order.
            new_notes (str): New notes text.
        """
        order = self.get_order_by_id_or_raise(order_id)

        try:
            order.notes = new_notes
            self.session.commit()
            logger.info(f"Order notes updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order notes: {e}")
            raise


    def delete_order(self, order_id: int) -> None:
        """
        Deletes an order by ID.

        Args:
            order_id (int): ID of the order to delete.
        """
        order = self.get_order_by_id_or_raise(order_id)

        try:
            self.session.delete(order)
            self.session.commit()
            logger.info(f"Order with id '{order_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order with id '{order_id}': {e}")
            raise


    def get_orders_by_status(self, status: str):
        """
        Retrieves all orders that match the given status.

        Args:
            status (str): Order status to filter by.

        Returns:
            list: List of matching Order instances.

        Raises:
            ValueError: If status is invalid.
        """
        if status.upper() not in OrderStatus.__members__:
            raise ValueError(f"Invalid order status: {status}")

        try:
            stmt = select(Order).where(Order.status == OrderStatus[status.upper()])
            return self.session.scalars(stmt).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving orders with status '{status}': {e}")
            return []
