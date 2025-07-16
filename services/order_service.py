import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.order import Order
from models.enums import OrderStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, session):
        self.session = session

    def get_order_by_id(self, order_id: int) -> Order | None:
        return self.session.scalars(
            select(Order).where(Order.id == order_id)
        ).first()

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
        if order_number is not None:
            existing_order = self.session.scalars(
                select(Order).where(Order.order_number == order_number)
            ).first()
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
        try:
            return self.session.scalars(select(Order)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving orders: {e}")
            return []

    def update_order_status(self, order_id: int, new_status: str) -> None:
        if new_status.upper() not in OrderStatus.__members__:
            raise ValueError(f"Invalid order status: {new_status}")

        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")

        try:
            order.status = OrderStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Order status updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order status: {e}")
            raise

    def update_order_reference(self, order_id: int, new_reference: str) -> None:
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")

        try:
            order.reference = new_reference
            self.session.commit()
            logger.info(f"Order reference updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order reference: {e}")
            raise

    def update_order_notes(self, order_id: int, new_notes: str) -> None:
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id {order_id} not found.")

        try:
            order.notes = new_notes
            self.session.commit()
            logger.info(f"Order notes updated successfully for id {order_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating order notes: {e}")
            raise

    def delete_order(self, order_id: int) -> None:
        order = self.get_order_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id '{order_id}' does not exist.")

        try:
            self.session.delete(order)
            self.session.commit()
            logger.info(f"Order with id '{order_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting order with id '{order_id}': {e}")
            raise


    def get_orders_by_status(self, status: str):
        if status.upper() not in OrderStatus.__members__:
            raise ValueError(f"Invalid order status: {status}")

        try:
            return self.session.scalars(
                select(Order).where(Order.status == OrderStatus[status.upper()])
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving orders with status '{status}': {e}")
            return []
