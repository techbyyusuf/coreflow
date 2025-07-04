from sqlalchemy import String, Float, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float)
    unit: Mapped[int] = mapped_column()
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())