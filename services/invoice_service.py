import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.invoice import Invoice
from models.enums import InvoiceStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceService:
    def __init__(self, session):
        self.session = session

    def get_invoice_by_id(self, invoice_id: int) -> Invoice | None:
        return self.session.scalars(
            select(Invoice).where(Invoice.id == invoice_id)
        ).first()

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

    def get_all_invoices(self):
        try:
            return self.session.scalars(select(Invoice)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoices: {e}")
            return []

    def update_invoice_status(self, invoice_id: int, new_status: str) -> None:
        if new_status.upper() not in InvoiceStatus.__members__:
            raise ValueError(f"Invalid invoice status: {new_status}")

        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found.")

        try:
            invoice.status = InvoiceStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Invoice status updated successfully for id {invoice_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating invoice status: {e}")
            raise

    def update_invoice_notes(self, invoice_id: int, new_notes: str) -> None:
        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found.")

        try:
            invoice.notes = new_notes
            self.session.commit()
            logger.info(f"Invoice notes updated successfully for id {invoice_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating invoice notes: {e}")
            raise

    def delete_invoice(self, invoice_id: int) -> None:
        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id '{invoice_id}' does not exist.")

        try:
            self.session.delete(invoice)
            self.session.commit()
            logger.info(f"Invoice with id '{invoice_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice with id '{invoice_id}': {e}")
            raise


    def get_invoices_by_status(self, status: str):
        if status.upper() not in InvoiceStatus.__members__:
            raise ValueError(f"Invalid invoice status: {status}")

        try:
            return self.session.scalars(
                select(Invoice).where(Invoice.status == InvoiceStatus[status.upper()])
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoices with status '{status}': {e}")
            return []
