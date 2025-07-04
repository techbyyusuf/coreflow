import re
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.models import User

class UserService:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Checks if the email address is valid using a simple regex pattern.
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None


    @staticmethod
    def is_valid_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True


    def create_user(self, name, email, password):
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address format")
        if not self.is_valid_password(password):
            raise ValueError(
                "Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        new_user = User(name=name, email=email, password=password)

        try:
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
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        try:
            user = self.session.scalars(select(User)).filter_by(id=user_id).first()
            if not user:
                raise ValueError(f"User with id {user_id} not found.")

            user.email = new_email
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            print(f"Error updating movie: {e}")
            raise


    def delete_user(self, user_id):
        user = self.session.scalars(select(User)).filter_by(id=user_id).first()

        try:
            if user:
                self.session.delete(user)
                self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            print(f"User with id '{user_id}' does not exist.")
            raise


# JWT login / token
# Week 8 Präsentation vorbereiten
# swagger docs