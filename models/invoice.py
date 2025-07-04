from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    invoice_number: Mapped[int] = mapped_column(unique=True)
    issue_date: Mapped[Date] = mapped_column(Date)
    due_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String)
    referee: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(String, nullable=True)