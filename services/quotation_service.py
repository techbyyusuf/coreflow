import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.quotation import Quotation
from models.enums import QuotationStatus
from models.customer import Customer
from models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuotationService:
    """
    Service class for managing quotations, including creation, update, retrieval, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_quotation_by_id_or_raise(self, quotation_id: int) -> Quotation | None:
        """
        Retrieves a quotation by ID or raises an error if not found.

        Args:
            quotation_id (int): ID of the quotation.

        Returns:
            Quotation: The found quotation.
        """
        stmt = select(Quotation).where(Quotation.id == quotation_id)
        quotation = self.session.scalars(stmt).first()

        if not quotation:
            raise ValueError(f"Quotation with id {quotation_id} not found.")
        return quotation


    def get_customer_or_raise(self, customer_id: int) -> Customer:
        """
        Retrieves a customer by ID or raises an error if not found.

        Args:
            customer_id (int): ID of the customer.

        Returns:
            Customer: The found customer.
        """
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = self.session.scalars(stmt).first()

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")
        return customer


    def get_user_or_raise(self, user_id: int) -> User:
        """
        Retrieves a user by ID or raises an error if not found.

        Args:
            user_id (int): ID of the user.

        Returns:
            User: The found user.
        """
        stmt = select(User).where(User.id == user_id)
        user = self.session.scalars(stmt).first()

        if not user:
            raise ValueError(f"User with id {user_id} not found.")
        return user


    def quotation_with_issue_date_exists(self, issue_date: str) -> Quotation:
        """
            Retrieves a quotation by issue_date or raises an error if not found.

        Args:
            issue_date (str): Issue date of quotation

        Returns:
            Quotation: The found quotation.
        """
        stmt = select(Quotation).where(Quotation.issue_date == issue_date)
        quotation = self.session.scalars(stmt).all()

        if not quotation:
            raise ValueError(f"Quotation with issue date '{issue_date}' not found.")
        return quotation


    def create_quotation(
        self,
        customer_id: int,
        user_id: int,
        issue_date,
        due_date=None,
        quotation_number: str = None,
        status: str = "DRAFT",
        notes: str = None
    ) -> None:
        """
        Creates a new quotation with optional metadata.

        Args:
            customer_id (int): ID of the customer.
            user_id (int): ID of the user creating the quotation.
            issue_date (date): Date the quotation is issued.
            due_date (date, optional): Expiration date of the quotation.
            quotation_number (str, optional): Unique identifier.
            status (str): Initial status.
            notes (str, optional): Additional notes.

        Raises:
            ValueError: If data is invalid or already in use.
        """
        self.get_customer_or_raise(customer_id)
        self.get_user_or_raise(user_id)

        if quotation_number is not None:
            stmt = select(Quotation).where(Quotation.quotation_number == quotation_number)
            existing_quotation = self.session.scalars(stmt).first()

            if existing_quotation:
                raise ValueError("Quotation number already in use.")

        if status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid quotation status: {status}")

        new_quotation = Quotation(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date,
            quotation_number=quotation_number,
            status=QuotationStatus[status.upper()],
            notes=notes
        )

        try:
            self.session.add(new_quotation)
            self.session.commit()
            logger.info(f"Quotation created successfully for customer id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating quotation: {e}")
            raise


    def get_all_quotations(self, status=None, customer_id=None) -> list[Quotation]:
        """
        Retrieves all quotations, optionally filtered by status or customer.

        Args:
            status (str, optional): Filter by status (e.g. 'DRAFT', 'SENT').
            customer_id (int, optional): Filter by customer ID.

        Returns:
            list: List of matching Quotation instances, or empty list if none found.
        """
        stmt = select(Quotation)

        if status:
            if status.upper() not in QuotationStatus.__members__:
                logger.warning(f"Invalid quotation status filter: '{status}'.")
                raise ValueError(f"Invalid quotation status: {status}")
            stmt = stmt.where(
                Quotation.status == QuotationStatus[status.upper()])

        if customer_id:
            self.get_customer_or_raise(customer_id)
            stmt = stmt.where(Quotation.customer_id == customer_id)

        try:
            return self.session.scalars(stmt).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotations: {e}")
            return []


    def update_quotation_status(self, quotation_id: int, new_status: str) -> None:
        """
        Updates the status of a quotation.

        Args:
            quotation_id (int): ID of the quotation.
            new_status (str): New status.

        Raises:
            ValueError: If status is invalid.
        """
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        if new_status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid quotation status: {new_status}")

        try:
            quotation.status = QuotationStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Quotation status updated successfully for id {quotation_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating quotation status: {e}")
            raise


    def update_quotation_notes(self, quotation_id: int, new_notes: str) -> None:
        """
        Updates the notes of a quotation.

        Args:
            quotation_id (int): ID of the quotation.
            new_notes (str): New notes text.
        """
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        try:
            quotation.notes = new_notes
            self.session.commit()
            logger.info(f"Quotation notes updated successfully for id {quotation_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating quotation notes: {e}")
            raise


    def delete_quotation(self, quotation_id: int) -> None:
        """
        Deletes a quotation by ID.

        Args:
            quotation_id (int): ID of the quotation to delete.
        """
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        try:
            self.session.delete(quotation)
            self.session.commit()
            logger.info(f"Quotation with id '{quotation_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting quotation with id '{quotation_id}': {e}")
            raise


    def get_quotations_by_status(self, status: str):
        """
        Retrieves all quotations filtered by status.

        Args:
            status (str): Quotation status to filter by.

        Returns:
            list: List of matching Quotation instances.

        Raises:
            ValueError: If status is invalid.
        """
        if status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid invoice status: {status}")

        try:
            stmt = select(Quotation).where(Quotation.status == QuotationStatus[status.upper()])
            return self.session.scalars(stmt).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotations with status '{status}': {e}")
            return []
