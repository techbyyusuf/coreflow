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
        """
        Initializes the UserService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Checks if the email address is valid using a simple regex pattern.

        :param email: Email string to validate
        :return: True if valid, False otherwise
        """
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    @staticmethod
    def is_valid_password(password: str) -> bool:
        """
        Checks if the password meets security requirements:
        - Minimum 8 characters
        - At least one digit
        - At least one special character

        :param password: Password string to validate
        :return: True if valid, False otherwise
        """
        if len(password) < 8:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def create_user(self,name: str,
                    email: str,
                    password: str,
                    role: str = "employee") -> None:
        """
        Creates a new user in the database after validating email and password.

        :param name: User's name
        :param email: User email
        :param password: User password
        :param role: user role, default: employee
        :raises ValueError: If email, password or role are invalid
        :raises SQLAlchemyError: If database error occurs
        """
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address format")
        if not self.is_valid_password(password):
            raise ValueError(
                "Password too weak (min. 8 chars, at least 1 digit, at least 1 special character)")

        existing_user = self.session.scalars(select(User).filter_by(
            email=email)).first()
        if existing_user:
            raise ValueError("Email address already in use.")

        role_upper = role.upper()
        if role_upper not in UserRole.__members__:
            raise ValueError(f"Invalid role: {role}")

        new_user = User(name=name, email=email, password=password,
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

        :return: List of User objects or empty list on error
        """
        try:
            return self.session.scalars(select(User)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving users: {e}")
            return []

    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a single user by ID.

        :param user_id: ID of the user
        :return: User object if found, otherwise None
        """
        logger.info(f"Searching for user with id '{user_id}'.")
        return self.session.scalars(select(User).filter_by(id=user_id)).first()


    def update_user_email(self, user_id: int, new_email: str) -> None:
        """
        Updates the email address of a user.

        :param user_id: ID of the user to update
        :param new_email: New email address
        :raises ValueError: If email is invalid or user not found
        :raises SQLAlchemyError: If database error occurs
        """
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        existing_user = self.session.scalars(select(User)).filter_by(
            email=new_email).first()
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
        Updates the password of a user after validating it.

        :param user_id: ID of the user to update
        :param new_password: New password
        :raises ValueError: If password is invalid or user not found
        :raises SQLAlchemyError: If database error occurs
        """
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
        """
        Deletes a user from the database.

        :param user_id: ID of the user to delete
        :raises ValueError: If user not found
        :raises SQLAlchemyError: If database error occurs
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
