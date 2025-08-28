from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import OrderStatus

class Order(Base):
    """
    Defines the Order model representing customer orders.

    Attributes:
        id (int): Primary key.
        customer_id (int): Foreign key referencing the customer.
        user_id (int): Foreign key referencing the user who created the order.
        issue_date (date): The date the order was issued.
        due_date (date): Optional due date for order fulfillment.
        delivery_date (date): Optional delivery date.
        order_number (str): Unique identifier for the order.
        status (OrderStatus): Status of the order (e.g., open, shipped).
        reference (str): Reference text.
        notes (str): Optional notes about the order.
        items (list[OrderItem]): Related order items.
    """

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    issue_date: Mapped[Date] = mapped_column(Date, nullable=False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    delivery_date: Mapped[Date] = mapped_column(Date, nullable=True)
    order_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    reference: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    items = relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )