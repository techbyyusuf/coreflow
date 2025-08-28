from sqlalchemy import String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Customer(Base):
    """
    Defines the Customer model for storing client-related information.

    Attributes:
        id (int): Primary key.
        name (str): Contact person's name.
        company_name (str): Unique company name.
        email (str): Unique email address.
        phone (str): Contact phone number.
        address (str): Mailing address.
        tax_id (str): Unique tax identification number.
        notes (str): Optional notes about the customer.
        created_at (datetime): Timestamp when the record was created.
    """

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable= True)
    company_name: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    tax_id: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
