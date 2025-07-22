from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_item import BaseItem

class QuotationItem(BaseItem):
    """
    Defines the QuotationItem model which inherits from BaseItem.

    Each quotation item is linked to a specific quotation via a foreign key.
    """

    __tablename__ = "quotation_items"

    quotation_id: Mapped[int] = mapped_column(ForeignKey("quotations.id"), nullable=False)
