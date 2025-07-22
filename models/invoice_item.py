from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_item import BaseItem

class InvoiceItem(BaseItem):
    """
    Defines the InvoiceItem model which inherits from BaseItem.

    Each invoice item is linked to a specific invoice via a foreign key.
    """

    __tablename__ = "invoice_items"

    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
