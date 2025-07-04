from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class OrderItem(Base):
    __tablename__ = "orderitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)