from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class BaseItem(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(nullable=False)
    unit_price: Mapped[float] = mapped_column(nullable=False)

