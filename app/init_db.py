import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    """
    Create all tables in the database.
    WARNING: Only use this on first setup or if you want to recreate all tables!
    """
    Base.metadata.create_all(engine)


def reset_db():
    """
    Drops all tables and recreates them.
    Use with caution: all data will be lost!
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ ==  "__main__":
    session = Session()
    session.close()
