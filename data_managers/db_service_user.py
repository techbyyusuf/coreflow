from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.models import User

class UserService:
    def __init__(self, session):
        self.session = session

    def create_user(self, name, email):
        try:
                                                                                    #e-mail checken!
                                                                                    #was ist mit den restlichen Daten?
            new_user = User(name=name, email=email)
            self.session.add(new_user)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            print(f"Username '{name}' already exists.")
            raise

    def get_all_users(self):
        try:
            return self.session.scalars(select(User)).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving users: {e}")
            return []


    def update_user_email(self, user_id, new_email):
        try:
            #erstmal email checken

            user = self.session.scalars(select(User)).filter_by(id=user_id).first()
            if user:
                user.email = new_email
                self.session.commit()
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            print(f"Error updating movie: {e}")
            raise

    def delete_user(self, user_id):
        try:
            user = self.session.scalars(select(User)).filter_by(id=user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            print(f"User with id '{user_id}' does not exist.")
            raise
