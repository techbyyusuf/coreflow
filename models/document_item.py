from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class DocumentItem(Base):
    __tablename__ = "documentitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable= False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable= False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable= False)