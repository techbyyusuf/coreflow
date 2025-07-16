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


    def get_customer_by_id(self, customer_id: int) -> Customer | None:
        """
        Retrieves a single customer by ID.

        :param customer_id: ID of the customer
        :return: Customer object if found, otherwise None
        """
        return self.session.scalars(
            select(Customer).filter_by(id=customer_id)).first()


    def create_customer(
        self,
        name: str = None,
        company_name: str = None,
        email: str = None,
        phone: str = None,
        address: str = None,
        tax_id: str = None,
        notes: str = None
    ) -> None:
        """
        Creates a new customer in the database after validating email.
        :param name: Customer name
        :param company_name: Customer company name
        :param email: Customer email
        :param phone: Phone number
        :param address: Address
        :param tax_id: Tax ID (must be unique)
        :param notes: Optional notes
        :raises ValueError: If email is invalid or neither name or company_name is not given
        :raises SQLAlchemyError: If database error occurs
        """

        if not name and not company_name:
            raise ValueError(
                "At least one of 'name' or 'company_name' must be provided.")

        if email is not None and not self.is_valid_email(email):
            raise ValueError("Invalid email address format")

        if email is not None:
            existing_customer = self.session.scalars(
                select(Customer)).filter_by(email=email).first()
            if existing_customer:
                raise ValueError("Email address already in use.")

        if company_name is not None:
            existing_customer = self.session.scalars(
                select(Customer)).filter_by(company_name=company_name).first()
            if existing_customer:
                raise ValueError("Company name already in use.")

        if tax_id is not None:
            existing_customer = self.session.scalars(
                select(Customer)).filter_by(tax_id=tax_id).first()
            if existing_customer:
                raise ValueError("Tax ID already in use.")

        new_customer = Customer(
            name=name,
            company_name=company_name,
            email=email,
            phone=phone,
            address=address,
            tax_id=tax_id,
            notes=notes
        )

        try:
            self.session.add(new_customer)
            self.session.commit()

            identifier = name if name else company_name
            logger.info(f"Customer '{identifier}' created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating customer '{name}': {e}")
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


    def update_customer_company_name(self, customer_id: int,
                                     new_company_name: str) -> None:
        """
        Updates the company name of a customer after checking uniqueness.

        :param customer_id: ID of the customer
        :param new_company_name: New company name
        :raises ValueError: If company name already in use or customer not found
        """
        existing_customer = self.session.scalars(select(Customer)).filter_by(
            company_name=new_company_name).first()
        if existing_customer and existing_customer.id != customer_id:
            raise ValueError("Company name already in use by another customer.")

        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.company_name = new_company_name
            self.session.commit()
            logger.info(
                f"Customer company name updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer company name: {e}")
            raise


    def update_customer_email(self, customer_id: int, new_email: str) -> None:
        """
        Updates the email address of a customer.
        :param customer_id: ID of the customer
        :param new_email: New email address
        :raises ValueError: If email is invalid or customer not found
        """
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        existing_customer = self.session.scalars(select(Customer)).filter_by(
            email=new_email).first()
        if existing_customer and existing_customer.id != customer_id:
            raise ValueError(
                "Email address already in use by another customer.")

        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.email = new_email
            self.session.commit()
            logger.info(f"Customer email updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer email: {e}")
            raise


    def update_customer_phone(self, customer_id: int, new_phone: str) -> None:
        """
        Updates the phone number of a customer.

        :param customer_id: ID of the customer
        :param new_phone: New phone number
        :raises ValueError: If customer not found
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.phone = new_phone
            self.session.commit()
            logger.info(
                f"Customer phone updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer phone: {e}")
            raise


    def update_customer_address(self, customer_id: int,
                                new_address: str) -> None:
        """
        Updates the address of a customer.

        :param customer_id: ID of the customer
        :param new_address: New address
        :raises ValueError: If customer not found
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.address = new_address
            self.session.commit()
            logger.info(
                f"Customer address updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer address: {e}")
            raise


    def update_customer_notes(self, customer_id: int, new_notes: str) -> None:
        """
        Updates the notes field of a customer.

        :param customer_id: ID of the customer
        :param new_notes: New notes
        :raises ValueError: If customer not found
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.notes = new_notes
            self.session.commit()
            logger.info(
                f"Customer notes updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer notes: {e}")
            raise


    def delete_customer(self, customer_id: int) -> None:
        """
        Deletes a customer from the database.
        :param customer_id: ID of the customer to delete
        :raises ValueError: If customer not found
        """
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(
                f"Customer with id '{customer_id}' does not exist.")

        try:
            self.session.delete(customer)
            self.session.commit()
            logger.info(f"Customer with id '{customer_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting customer with id '{customer_id}': {e}")
            raise
