from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Base class for all ORM models using SQLAlchemy's DeclarativeBase.
    All models should inherit from this class.
    """
    pass