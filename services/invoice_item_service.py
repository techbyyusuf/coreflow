import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.invoice_item import InvoiceItem

logger = logging.getLogger(__name__)


class InvoiceItemService:
    """
    Service class for handling CRUD operations related to InvoiceItem.
    """

    def __init__(self, session):
        """
        Initializes the InvoiceItemService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_invoice_item(self, invoice_id: int, product_id: int,
                            quantity: int, unit_price: float) -> None:
        """
        Creates a new invoice item in the database.

        :param invoice_id: ID of the related invoice
        :param product_id: ID of the related product
        :param quantity: Quantity of the product
        :param unit_price: Unit price at the time of invoicing
        :raises SQLAlchemyError: If database error occurs
        """
        new_item = InvoiceItem(
            invoice_id=invoice_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_item)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating invoice item for invoice {invoice_id}: {e}")
            raise

    def get_all_invoice_items(self):
        """
        Retrieves all invoice items from the database.

        :return: List of InvoiceItem objects or empty list on error
        """
        try:
            return self.session.scalars(select(InvoiceItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoice items: {e}")
            return []

    def update_invoice_item_quantity(self, item_id: int, new_quantity: int) -> None:
        """
        Updates the quantity of an invoice item.

        :param item_id: ID of the invoice item to update
        :param new_quantity: New quantity value
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(InvoiceItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Invoice item with id '{item_id}' not found.")

            item.quantity = new_quantity
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating invoice item quantity: {e}")
            raise

    def delete_invoice_item(self, item_id: int) -> None:
        """
        Deletes an invoice item from the database.

        :param item_id: ID of the item to delete
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(InvoiceItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Invoice item with id '{item_id}' does not exist.")

            self.session.delete(item)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice item with id '{item_id}': {e}")
            raise
