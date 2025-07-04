from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Base, User

engine = create_engine("postgresql+psycopg2://myuser:mypassword@db:5432/mydatabase")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

