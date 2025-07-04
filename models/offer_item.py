from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class OfferItem(Base):
    __tablename__ = "offeritems"

    id: Mapped[int] = mapped_column(primary_key=True)
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)