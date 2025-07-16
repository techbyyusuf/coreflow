from sqlalchemy import String, Float, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.enums import UnitType

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable= False, unique=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float, nullable= False)
    unit: Mapped[UnitType] = mapped_column(Enum(UnitType), nullable= False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())