from sqlalchemy import String, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.enums import DocumentType, DocumentStatus

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType), nullable= False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable= False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable= False)
    issue_date: Mapped[Date] = mapped_column(Date, nullable= False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=True)
    delivery_date: Mapped[Date] = mapped_column(Date, nullable=True)
    invoice_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus), nullable= False)
    reference: Mapped[str] = mapped_column(String, nullable=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)