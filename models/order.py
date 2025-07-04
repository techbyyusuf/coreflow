from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    issue_date: Mapped[Date] = mapped_column(Date)
    delivery_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(String, nullable=True)