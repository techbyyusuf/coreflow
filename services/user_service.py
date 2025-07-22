import re
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.user import User
from models.enums import UserRole
from security.password_manager import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserService:
    """
    Service class for handling user creation, validation, retrieval, updates, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates if the email has a proper format.

        Args:
            email (str): Email address.

        Returns:
            bool: True if valid, else False.
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None


    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Validates if the password meets strength requirements.

        Args:
            password (str): Password to validate.

        Returns:
            bool: True if valid, else False.
        """
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True


    def raise_if_user_email_exists(self, user_email) -> None:
        """
        Raises an error if a user with the given email already exists.

        Args:
            user_email (str): Email address to check.
        """
        stmt = select(User).where(User.email == user_email)
        user = self.session.scalars(stmt).first()

        if user:
            raise ValueError("Email address already in use.")
        return None


    def create_user(self, name: str, email: str, password: str, role: str = "employee") -> None:
        """
        Creates a new user after performing validations.

        Args:
            name (str): Full name.
            email (str): Email address.
            password (str): Raw password.
            role (str): User role (default: employee).

        Raises:
            ValueError: If inputs are invalid or already in use.
        """
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address format")
        if not self.is_valid_password(password):
            raise ValueError("Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        self.raise_if_user_email_exists(email)

        role_upper = role.upper()
        if role_upper not in UserRole.__members__:
            raise ValueError(f"Invalid role: {role}")

        hashed_pw = hash_password(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_pw,
            role=UserRole[role_upper])

        try:
            self.session.add(new_user)
            self.session.commit()
            logger.info(f"User '{name}' created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating user '{name}': {e}")
            raise


    def get_all_users(self) -> list[User]:
        """
        Retrieves all users from the database.

        Returns:
            list[User]: List of user objects.
        """
        try:
            return self.session.scalars(select(User)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving users: {e}")
            return []


    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): ID of the user.

        Returns:
            User | None: The found user, or None if not found.
        """
        logger.info(f"Searching for user with id '{user_id}'.")
        return self.session.scalars(
            select(User).where(User.id == user_id)
        ).first()


    def update_user_email(self, user_id: int, new_email: str) -> None:
        """
        Updates the email address of a user.

        Args:
            user_id (int): ID of the user.
            new_email (str): New email address.

        Raises:
            ValueError: If the email is invalid or already in use.
        """
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
        """
        Updates the password of a user.

        Args:
            user_id (int): ID of the user.
            new_password (str): New password.

        Raises:
            ValueError: If the password is invalid.
        """
        if not self.is_valid_password(new_password):
            raise ValueError("Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with id '{user_id}' not found.")

        try:
            hashed_password = hash_password(new_password)
            user.password = hashed_password
            self.session.commit()
            logger.info(f"User password updated successfully for id '{user.id}'.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating user password: {e}")
            raise


    def delete_user(self, user_id: int) -> None:
        """
        Deletes a user by ID.

        Args:
            user_id (int): ID of the user to delete.

        Raises:
            ValueError: If the user does not exist.
        """
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
