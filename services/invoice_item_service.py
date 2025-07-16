import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.invoice_item import InvoiceItem
from models.invoice import Invoice

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceItemService:
    def __init__(self, session):
        self.session = session

    def get_invoice_by_id(self, invoice_id: int):
        return self.session.scalars(
            select(Invoice).where(Invoice.id == invoice_id)
        ).first()

    def get_item_by_id(self, item_id: int):
        return self.session.scalars(
            select(InvoiceItem).where(InvoiceItem.id == item_id)
        ).first()

    def create_item(self, invoice_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice with id {invoice_id} not found.")

        new_item = InvoiceItem(
            invoice_id=invoice_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_item)
            self.session.commit()
            logger.info(f"Item created successfully for invoice id {invoice_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating invoice item: {e}")
            raise

    def update_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found.")

        try:
            item.quantity = new_quantity
            item.unit_price = new_unit_price
            self.session.commit()
            logger.info(f"Invoice item updated successfully for id {item_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating invoice item: {e}")
            raise

    def delete_item(self, item_id: int) -> None:
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id '{item_id}' does not exist.")

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Invoice item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice item with id '{item_id}': {e}")
            raise

    def get_all_items(self):
        try:
            return self.session.scalars(select(InvoiceItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoice items: {e}")
            return []
