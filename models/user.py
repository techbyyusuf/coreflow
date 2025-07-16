from sqlalchemy import String, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable= False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable= False)
    password: Mapped[str] = mapped_column(String, nullable= False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable= False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())