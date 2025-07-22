from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class BaseItem(Base):
    """
    Abstract base class for items used in documents such as invoices, orders, and quotations.

    Attributes:
        id (int): Primary key of the item.
        product_id (int): Foreign key referencing the product.
        quantity (float): Quantity of the product.
        unit_price (float): Price per unit.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)

