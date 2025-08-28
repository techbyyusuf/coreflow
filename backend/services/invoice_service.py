import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from sqlalchemy.orm import selectinload

from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from models.enums import InvoiceStatus
from models.customer import Customer
from models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceService:
    """
    Service class for managing invoice operations such as creation, update, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_invoice_by_id_or_raise(self, invoice_id: int) -> Invoice:
        """
        Retrieves an invoice by ID or raises a ValueError if not found.

        Args:
            invoice_id (int): ID of the invoice.

        Returns:
            Invoice: The found invoice instance.
        """
        stmt = select(Invoice).where(Invoice.id == invoice_id)
        invoice = self.session.scalars(stmt).first()

        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found.")
        return invoice


    def get_invoice_by_id_with_product(self, invoice_id: int) -> Invoice:
        """
        Retrieves an invoice by ID or raises a ValueError if not found.

        Args:
            invoice_id (int): ID of the invoice.

        Returns:
            Invoice: The found invoice instance.
        """
        stmt = (select(Invoice)
                .options(
            selectinload(Invoice.items).joinedload(InvoiceItem.product)
        )
                .where(Invoice.id == invoice_id))
        invoice = self.session.scalars(stmt).first()

        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found.")
        return invoice


    def get_customer_or_raise(self, customer_id: int) -> Customer:
        """
        Retrieves a customer by ID or raises a ValueError if not found.

        Args:
            customer_id (int): ID of the customer.

        Returns:
            Customer: The found customer instance.
        """
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = self.session.scalars(stmt).first()

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")
        return customer


    def get_user_or_raise(self, user_id: int) -> User:
        """
        Retrieves a user by ID or raises a ValueError if not found.

        Args:
            user_id (int): ID of the user.

        Returns:
            User: The found user instance.
        """
        stmt = select(User).where(User.id == user_id)
        user = self.session.scalars(stmt).first()

        if not user:
            raise ValueError(f"User with id {user_id} not found.")
        return user


    def create_invoice(
        self,
        customer_id: int,
        user_id: int,
        issue_date,
        due_date=None,
        invoice_number=None,
        status: str = "DRAFT",
        notes: str = None
    ) -> None:
        """
        Creates a new invoice with optional fields and validations.

        Args:
            customer_id (int): ID of the customer.
            user_id (int): ID of the user.
            issue_date (date): Invoice issue date.
            due_date (date, optional): Due date.
            invoice_number (str, optional): Unique invoice number.
            status (str): Status string, must match InvoiceStatus.
            notes (str, optional): Notes.

        Raises:
            ValueError: If status or invoice_number is invalid or already in use.
        """
        self.get_customer_or_raise(customer_id)
        self.get_user_or_raise(user_id)

        if status.upper() not in InvoiceStatus.__members__:
            raise ValueError(f"Invalid invoice status: {status}")

        if invoice_number is not None:
            existing_invoice = self.session.scalars(
                select(Invoice).where(Invoice.invoice_number == invoice_number)
            ).first()
            if existing_invoice:
                raise ValueError("Invoice number already in use.")

        new_invoice = Invoice(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date,
            invoice_number=invoice_number,
            status=InvoiceStatus[status.upper()],
            notes=notes
        )

        try:
            self.session.add(new_invoice)
            self.session.commit()
            logger.info(f"Invoice created successfully for customer id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating invoice: {e}")
            raise

    def get_all_invoices(
            self,
            status: Optional[str] = None,
            invoice_number: Optional[str] = None,
            customer_id: Optional[int] = None
    ) -> list[Invoice]:
        """
        Retrieves all invoices, optionally filtered by status, invoice number, or customer ID.

        Args:
            status (str, optional): Filter by invoice status.
            invoice_number (str, optional): Filter by invoice number.
            customer_id (int, optional): Filter by customer ID.

        Returns:
            list[Invoice]: List of matching Invoice instances.
        """
        stmt = select(Invoice)

        if status:
            if status.upper() not in InvoiceStatus.__members__:
                logger.warning(f"Invalid invoice status: '{status}'")
                raise ValueError(f"Invalid invoice status: {status}")
            stmt = stmt.where(Invoice.status == InvoiceStatus[status.upper()])

        if invoice_number:
            stmt = stmt.where(Invoice.invoice_number == invoice_number)

        if customer_id:
            stmt = stmt.where(Invoice.customer_id == customer_id)

        try:
            return self.session.scalars(stmt).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoices: {e}")
            return []

    def update_invoice_status(self, invoice_id: int, new_status: str) -> None:
        """
        Updates the status of an invoice.

        Args:
            invoice_id (int): Invoice ID.
            new_status (str): New status value.

        Raises:
            ValueError: If new_status is invalid.
        """
        invoice = self.get_invoice_by_id_or_raise(invoice_id)

        if new_status.upper() not in InvoiceStatus.__members__:
            raise ValueError(f"Invalid invoice status: {new_status}")

        try:
            invoice.status = InvoiceStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Invoice status updated successfully for id {invoice_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating invoice status: {e}")
            raise


    def update_invoice_notes(self, invoice_id: int, new_notes: str) -> None:
        """
        Updates the notes of an invoice.

        Args:
            invoice_id (int): Invoice ID.
            new_notes (str): New notes.
        """
        invoice = self.get_invoice_by_id_or_raise(invoice_id)

        try:
            invoice.notes = new_notes
            self.session.commit()
            logger.info(f"Invoice notes updated successfully for id {invoice_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating invoice notes: {e}")
            raise


    def delete_invoice(self, invoice_id: int) -> None:
        """
        Deletes an invoice by ID.

        Args:
            invoice_id (int): ID of the invoice to delete.
        """
        invoice = self.get_invoice_by_id_or_raise(invoice_id)

        try:
            self.session.delete(invoice)
            self.session.commit()
            logger.info(f"Invoice with id '{invoice_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice with id '{invoice_id}': {e}")
            raise


    def get_invoices_by_status(self, status: str):
        """
        Retrieves all invoices filtered by status.

        Args:
            status (str): The invoice status to filter by.

        Returns:
            list: List of matching Invoice instances.

        Raises:
            ValueError: If status is invalid.
        """
        if status.upper() not in InvoiceStatus.__members__:
            raise ValueError(f"Invalid invoice status: {status}")

        try:
            return self.session.scalars(
                select(Invoice).where(Invoice.status == InvoiceStatus[status.upper()])
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoices with status '{status}': {e}")
            return []
