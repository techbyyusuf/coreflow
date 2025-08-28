import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.invoice_item import InvoiceItem
from models.invoice import Invoice
from models.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InvoiceItemService:
    """
    Service class for managing items associated with invoices.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_invoice_or_raise(self, invoice_id: int):
        """
        Retrieves an invoice by ID or raises an error if not found.

        Args:
            invoice_id (int): The ID of the invoice to retrieve.

        Returns:
            Invoice: The found invoice.
        """
        stmt = select(Invoice).where(Invoice.id == invoice_id)
        invoice = self.session.scalars(stmt).first()

        if not invoice:
            raise ValueError(f"Invoice with id '{invoice_id}' not found.")
        return invoice


    def get_product_or_raise(self, product_id: int):
        """
        Retrieves a product by ID or raises an error if not found.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Product: The found product.
        """
        stmt = select(Product).where(Product.id == product_id)
        product = self.session.scalars(stmt).first()

        if not product:
            raise ValueError(f"Product with id '{product_id}' not found.")
        return product


    def get_item_by_id_or_raise(self, item_id: int):
        """
        Retrieves an invoice item by ID or raises an error if not found.

        Args:
            item_id (int): The ID of the invoice item.

        Returns:
            InvoiceItem: The found invoice item.
        """
        stmt = select(InvoiceItem).where(InvoiceItem.id == item_id)
        item = self.session.scalars(stmt).first()

        if not item:
            raise ValueError(f"Item with id '{item_id}' not found.")
        return item


    def get_all_items(self):
        """
        Retrieves all invoice items from the database.

        Returns:
            list: List of all InvoiceItem instances.
        """
        try:
            return self.session.scalars(select(InvoiceItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving invoice items: {e}")
            return []


    def create_item(self, invoice_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        """
        Creates a new invoice item.

        Args:
            invoice_id (int): The invoice the item belongs to.
            product_id (int): The associated product.
            quantity (float): Quantity of the product.
            unit_price (float): Price per unit.

        Raises:
            ValueError: If quantity or price is negative or foreign key targets don't exist.
        """
        self.get_invoice_or_raise(invoice_id)
        self.get_product_or_raise(product_id)

        if quantity < 0:
            raise ValueError("Quantity must be zero or positive.")
        if unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

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
        """
        Updates quantity and unit price of an existing invoice item.

        Args:
            item_id (int): ID of the invoice item to update.
            new_quantity (float): New quantity.
            new_unit_price (float): New unit price.

        Raises:
            ValueError: If quantity or price is negative.
        """
        item = self.get_item_by_id_or_raise(item_id)

        if new_quantity < 0:
            raise ValueError("Quantity must be zero or positive.")
        if new_unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

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
        """
        Deletes an invoice item by ID.

        Args:
            item_id (int): ID of the invoice item to delete.
        """
        item = self.get_item_by_id_or_raise(item_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Invoice item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting invoice item with id '{item_id}': {e}")
            raise
