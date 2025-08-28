from sqlalchemy import String, Float, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.enums import UnitType
from models.invoice_item import InvoiceItem

class Product(Base):
    """
    Defines the Product model representing items that can be sold.

    Attributes:
        id (int): Primary key.
        name (str): Unique product name.
        description (str): Optional description of the product.
        unit_price (float): Price per unit of the product.
        unit (UnitType): Unit of measurement (e.g., piece, kg).
        created_at (datetime): Timestamp when the product was added.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable= False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float, nullable= False)
    unit: Mapped[UnitType] = mapped_column(Enum(UnitType), nullable= False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())

    items: Mapped[list["InvoiceItem"]] = relationship("InvoiceItem", back_populates="product")