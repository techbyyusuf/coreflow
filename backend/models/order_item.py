from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base_item import BaseItem

class OrderItem(BaseItem):
    """
    Defines the OrderItem model which inherits from BaseItem.

    Each order item is linked to a specific order via a foreign key.
    """

    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
