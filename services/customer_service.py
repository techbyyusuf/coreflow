import re
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.customer import Customer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomerService:
    """
    Service class for handling CRUD operations and validations related to Customer.
    """

    def __init__(self, session):
        """
        Initializes the CustomerService with a database session.
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


    def create_customer(
        self,
        user_id: int,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        address: str,
        tax_id: int,
        notes: str = None
    ) -> None:
        """
        Creates a new customer in the database after validating email.
        :param user_id: ID of the related user
        :param first_name: Customer first name
        :param last_name: Customer last name
        :param email: Customer email
        :param phone: Phone number
        :param address: Address
        :param tax_id: Tax ID (must be unique)
        :param notes: Optional notes
        :raises ValueError: If email is invalid
        :raises SQLAlchemyError: If database error occurs
        """
        if not self.is_valid_email(email):
            raise ValueError("Invalid email address format")

        new_customer = Customer(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            tax_id=tax_id,
            notes=notes
        )

        try:
            self.session.add(new_customer)
            self.session.commit()
            logger.info(f"Customer '{first_name} {last_name}' created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating customer '{first_name} {last_name}': {e}")
            raise


    def get_all_customers(self):
        """
        Retrieves all customers from the database.
        :return: List of Customer objects or empty list on error
        """
        try:
            return self.session.scalars(select(Customer)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving customers: {e}")
            return []


    def update_customer_email(self, customer_id: int, new_email: str) -> None:
        """
        Updates the email address of a customer.
        :param customer_id: ID of the customer
        :param new_email: New email address
        :raises ValueError: If email is invalid or customer not found
        """
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")

            customer.email = new_email
            self.session.commit()
            logger.info(f"Customer email updated successfully for id {customer_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating customer email: {e}")
            raise


    def update_customer_phone(self, customer_id: int, new_phone: str) -> None:
        """
        Updates the phone number of a customer.
        """
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")

            customer.phone = new_phone
            self.session.commit()
            logger.info(f"Customer phone updated successfully for id {customer_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating customer phone: {e}")
            raise


    def update_customer_address(self, customer_id: int, new_address: str) -> None:
        """
        Updates the address of a customer.
        """
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")

            customer.address = new_address
            self.session.commit()
            logger.info(f"Customer address updated successfully for id {customer_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating customer address: {e}")
            raise


    def update_customer_notes(self, customer_id: int, new_notes: str) -> None:
        """
        Updates the notes field of a customer.
        """
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id {customer_id} not found.")

            customer.notes = new_notes
            self.session.commit()
            logger.info(f"Customer notes updated successfully for id {customer_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating customer notes: {e}")
            raise


    def delete_customer(self, customer_id: int) -> None:
        """
        Deletes a customer from the database.
        :param customer_id: ID of the customer to delete
        :raises ValueError: If customer not found
        """
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if not customer:
                raise ValueError(f"Customer with id '{customer_id}' does not exist.")

            self.session.delete(customer)
            self.session.commit()
            logger.info(f"Customer with id '{customer_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting customer with id '{customer_id}': {e}")
            raise
