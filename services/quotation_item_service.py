import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.quotation_item import QuotationItem
from models.quotation import Quotation
from models.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuotationItemService:
    """
    Service class for managing items associated with quotations.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def get_quotation_or_raise(self, quotation_id: int):
        """
        Retrieves a quotation by ID or raises an error if not found.

        Args:
            quotation_id (int): The ID of the quotation.

        Returns:
            Quotation: The found quotation.
        """
        stmt = select(Quotation).where(Quotation.id == quotation_id)
        quotation = self.session.scalars(stmt).first()

        if not quotation:
            raise ValueError(f"Quotation with id {quotation_id} not found.")
        return quotation


    def get_product_or_raise(self, product_id: int):
        """
        Retrieves a product by ID or raises an error if not found.

        Args:
            product_id (int): The ID of the product.

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
        Retrieves a quotation item by ID or raises an error if not found.

        Args:
            item_id (int): The ID of the item.

        Returns:
            QuotationItem: The found item.
        """
        stmt = select(QuotationItem).where(QuotationItem.id == item_id)
        item = self.session.scalars(stmt).first()

        if not item:
            raise ValueError(f"Item with id {item_id} not found.")
        return item


    def create_item(self, quotation_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        """
        Creates a new quotation item.

        Args:
            quotation_id (int): ID of the quotation.
            product_id (int): ID of the product.
            quantity (float): Quantity of the product.
            unit_price (float): Unit price of the product.

        Raises:
            ValueError: If input values are invalid.
        """
        self.get_quotation_or_raise(quotation_id)
        self.get_product_or_raise(product_id)

        if quantity < 0:
            raise ValueError("Quantity must be zero or positive.")
        if unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

        new_item = QuotationItem(
            quotation_id=quotation_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_item)
            self.session.commit()
            logger.info(f"Item created successfully for quotation id {quotation_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating quotation item: {e}")
            raise


    def get_all_items(self):
        """
        Retrieves all quotation items from the database.

        Returns:
            list: List of QuotationItem instances.
        """
        try:
            return self.session.scalars(select(QuotationItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotation items: {e}")
            return []


    def update_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        """
        Updates quantity and unit price of an existing quotation item.

        Args:
            item_id (int): ID of the item.
            new_quantity (float): New quantity.
            new_unit_price (float): New unit price.

        Raises:
            ValueError: If values are invalid.
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
            logger.info(f"Quotation item updated successfully for id {item_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating quotation item: {e}")
            raise


    def delete_item(self, item_id: int) -> None:
        """
        Deletes a quotation item by ID.

        Args:
            item_id (int): ID of the item to delete.
        """
        item = self.get_item_by_id_or_raise(item_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Quotation item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting quotation item with id '{item_id}': {e}")
            raise
