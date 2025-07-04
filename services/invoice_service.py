import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.invoice import Invoice

logger = logging.getLogger(__name__)


class InvoiceService:
    """
    Service class for handling CRUD operations related to Invoice.
    """

    def __init__(self, session):
        """
        Initializes the InvoiceService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_invoice(self, customer_id: int, user_id: int, invoice_number: int,
                       issue_date, due_date, status: str, referee: str, notes: str = None) -> None:
        """
        Creates a new invoice in the database.

        :param customer_id: ID of the customer
        :param user_id: ID of the user
        :param invoice_number: Unique invoice number
        :param issue_date: Issue date of the invoice
        :param due_date: Due date for payment
        :param status: Status of the invoice
        :param referee: Referee information
        :param notes: Optional notes
        :raises SQLAlchemyError: If database error occurs
        """
        new_invoice = Invoice(
            customer_id=customer_id,
            user_id=user_id,
            invoice_number=invoice_number,
            issue_date=issue_date,
            due_date=due_date,
            status=status,
            referee=referee,
            notes=notes
        )

        try:
            self.session.add(new_invoice)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating invoice {invoice_number}: {e}")
            raise

    def get_all_invoices(self):
        """
        Retrieves all invoices from the database.

        :return: List of Invoice objects or empty list on error
        """
        try:
            return self.session.scalars(select(Invoice)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoices: {e}")
            return []

    def update_invoice_status(self, invoice_id: int, new_status: str) -> None:
        """
        Updates the status of an invoice.

        :param invoice_id: ID of the invoice to update
        :param new_status: New status value
        :raises ValueError: If invoice not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            invoice = self.session.scalars(select(Invoice)).filter_by(id=invoice_id).first()
            if not invoice:
                raise ValueError(f"Invoice with id '{invoice_id}' not found.")

            invoice.status = new_status
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating invoice status: {e}")
            raise

    def delete_invoice(self, invoice_id: int) -> None:
        """
        Deletes an invoice from the database.

        :param invoice_id: ID of the invoice to delete
        :raises ValueError: If invoice not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            invoice = self.session.scalars(select(Invoice)).filter_by(id=invoice_id).first()
            if not invoice:
                raise ValueError(f"Invoice with id '{invoice_id}' does not exist.")

            self.session.delete(invoice)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice with id '{invoice_id}': {e}")
            raise
