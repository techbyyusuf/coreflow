from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import QuotationStatus

class Quotation(Base):
    """
    Defines the Quotation model representing sales offers to customers.

    Attributes:
        id (int): Primary key.
        customer_id (int): Foreign key referencing the customer.
        user_id (int): Foreign key referencing the user who created the quotation.
        issue_date (date): Date the quotation was issued.
        due_date (date): Optional expiry date of the quotation.
        quotation_number (str): Unique identifier for the quotation.
        status (QuotationStatus): Current status of the quotation.
        notes (str): Optional notes regarding the quotation.
        items (list[QuotationItem]): Related quotation items.
    """

    __tablename__ = "quotations"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    issue_date: Mapped[Date] = mapped_column(Date, nullable=False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    quotation_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    status: Mapped[QuotationStatus] = mapped_column(Enum(QuotationStatus), nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    items = relationship("QuotationItem", backref="order", cascade="all, delete-orphan")