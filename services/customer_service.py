import re
import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.customer import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CustomerService:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def get_customer_by_id(self, customer_id: int) -> Customer | None:
        return self.session.scalars(
            select(Customer).where(Customer.id == customer_id)
        ).first()

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
        if not name and not company_name:
            raise ValueError("At least one of 'name' or 'company_name' must be provided.")

        if email is not None and not self.is_valid_email(email):
            raise ValueError("Invalid email address format")

        if email is not None:
            existing_customer = self.session.scalars(
                select(Customer).where(Customer.email == email)
            ).first()
            if existing_customer:
                raise ValueError("Email address already in use.")

        if company_name is not None:
            existing_customer = self.session.scalars(
                select(Customer).where(Customer.company_name == company_name)
            ).first()
            if existing_customer:
                raise ValueError("Company name already in use.")

        if tax_id is not None:
            existing_customer = self.session.scalars(
                select(Customer).where(Customer.tax_id == tax_id)
            ).first()
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
        try:
            return self.session.scalars(select(Customer)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving customers: {e}")
            return []

    def update_customer_company_name(self, customer_id: int, new_company_name: str) -> None:
        existing_customer = self.session.scalars(
            select(Customer).where(Customer.company_name == new_company_name)
        ).first()
        if existing_customer and existing_customer.id != customer_id:
            raise ValueError("Company name already in use by another customer.")

        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.company_name = new_company_name
            self.session.commit()
            logger.info(f"Customer company name updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer company name: {e}")
            raise

    def update_customer_email(self, customer_id: int, new_email: str) -> None:
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email address format")

        existing_customer = self.session.scalars(
            select(Customer).where(Customer.email == new_email)
        ).first()
        if existing_customer and existing_customer.id != customer_id:
            raise ValueError("Email address already in use by another customer.")

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
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.phone = new_phone
            self.session.commit()
            logger.info(f"Customer phone updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer phone: {e}")
            raise

    def update_customer_address(self, customer_id: int, new_address: str) -> None:
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.address = new_address
            self.session.commit()
            logger.info(f"Customer address updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer address: {e}")
            raise

    def update_customer_notes(self, customer_id: int, new_notes: str) -> None:
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")

        try:
            customer.notes = new_notes
            self.session.commit()
            logger.info(f"Customer notes updated successfully for id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating customer notes: {e}")
            raise

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with id '{customer_id}' does not exist.")

        try:
            self.session.delete(customer)
            self.session.commit()
            logger.info(f"Customer with id '{customer_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting customer with id '{customer_id}': {e}")
            raise
