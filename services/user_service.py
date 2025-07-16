import re
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.user import User
from models.enums import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    """
    Service class for handling CRUD operations and validations related to User.
    """

    def __init__(self, session):
        self.session = session

    @staticmethod
    def is_valid_email(email: str) -> bool:
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

    def raise_if_user_email_exists(self, user_email) -> None:
        stmt = select(User).where(User.email == user_email)
        user = self.session.scalars(stmt).first()

        if user:
            raise ValueError("Email address already in use.")
        return None


    def create_user(self, name: str, email: str, password: str, role: str = "employee") -> None:
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address format")
        if not self.is_valid_password(password):
            raise ValueError("Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        self.raise_if_user_email_exists(email)

        role_upper = role.upper()
        if role_upper not in UserRole.__members__:
            raise ValueError(f"Invalid role: {role}")

        new_user = User(name=name, email=email, password=password, role=UserRole[role_upper])

        try:
            self.session.add(new_user)
            self.session.commit()
            logger.info(f"User '{name}' created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating user '{name}': {e}")
            raise


    def get_all_users(self) -> list[User]:
        try:
            return self.session.scalars(select(User)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving users: {e}")
            return []


    def get_user_by_id(self, user_id: int) -> User | None:
        logger.info(f"Searching for user with id '{user_id}'.")
        return self.session.scalars(
            select(User).where(User.id == user_id)
        ).first()


    def update_user_email(self, user_id: int, new_email: str) -> None:
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        existing_user = self.session.scalars(
            select(User).where(User.email == new_email)
        ).first()
        if existing_user and existing_user.id != user_id:
            raise ValueError("Email address already in use by another user.")

        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found.")

        try:
            user.email = new_email
            self.session.commit()
            logger.info(f"User email updated successfully for id '{user.id}'.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating user email: {e}")
            raise


    def update_user_password(self, user_id: int, new_password: str) -> None:
        if not self.is_valid_password(new_password):
            raise ValueError("Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' not found.")

        try:
            user.password = new_password
            self.session.commit()
            logger.info(f"User password updated successfully for id '{user.id}'.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating user password: {e}")
            raise


    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' does not exist.")

        try:
            self.session.delete(user)
            self.session.commit()
            logger.info(f"User with id '{user.id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting user with id '{user_id}': {e}")
            raise
