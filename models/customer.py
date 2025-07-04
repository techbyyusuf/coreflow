from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    tax_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())