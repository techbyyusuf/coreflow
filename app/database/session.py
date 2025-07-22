import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """
    Initializes the database by creating all defined tables.

    WARNING:
        This should only be run during first setup or if you want to recreate all tables.
        Existing data will remain intact.
    """
    Base.metadata.create_all(engine)


def delete_db():
    """
    Drops all tables in the database.

    WARNING:
        This will permanently delete all data. Use only in development or reset scenarios.
    """
    Base.metadata.drop_all(bind=engine)


def get_db():
    """
    Dependency function for FastAPI routes.

    Yields:
        Session: A SQLAlchemy database session.
        Ensures the session is closed after the request finishes.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    session = Session()
    session.close()
