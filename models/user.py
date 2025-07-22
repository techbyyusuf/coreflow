from sqlalchemy import String, TIMESTAMP, func, Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.enums import UserRole

class User(Base):
    """
    Defines the User model for system authentication and authorization.

    Attributes:
        id (int): Primary key.
        name (str): Full name of the user.
        email (str): Unique email used for login.
        password (str): Hashed password.
        role (UserRole): Role assigned to the user (ADMIN, EMPLOYEE, VIEWER).
        created_at (datetime): Timestamp when the user was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable= False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable= False)
    password: Mapped[str] = mapped_column(String, nullable= False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable= False)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())