from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import InvoiceStatus

class Invoice(Base):
    """
    Defines the Invoice model representing billing documents.

    Attributes:
        id (int): Primary key.
        customer_id (int): Foreign key referencing the customer.
        user_id (int): Foreign key referencing the user who issued the invoice.
        issue_date (date): The date the invoice was created.
        due_date (date): Optional due date for payment.
        invoice_number (str): Unique invoice identifier.
        status (InvoiceStatus): Status of the invoice (e.g., sent, paid).
        notes (str): Optional notes regarding the invoice.
        items (list[InvoiceItem]): Related invoice items.
    """

    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    issue_date: Mapped[Date] = mapped_column(Date, nullable=False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    invoice_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    status: Mapped[InvoiceStatus] = mapped_column(Enum(InvoiceStatus), nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    items = relationship("InvoiceItem", backref="order", cascade="all, delete-orphan")