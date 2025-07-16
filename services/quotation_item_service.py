import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.quotation_item import QuotationItem
from models.quotation import Quotation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuotationItemService:
    def __init__(self, session):
        self.session = session


    def validate_quotation_exists(self, quotation_id: int):
        stmt = select(Quotation).where(Quotation.id == quotation_id)
        quotation =  self.session.scalars(stmt).first()

        if not quotation:
            raise ValueError(f"Quotation with id {quotation_id} not found.")
        return quotation


    def get_item_by_id(self, item_id: int):
        stmt = select(QuotationItem).where(QuotationItem.id == item_id)
        item =  self.session.scalars(stmt).first()

        if not item:
            raise ValueError(f"Item with id {item_id} not found.")
        return item


    def create_item(self, quotation_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        self.validate_quotation_exists(quotation_id)

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


    def update_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        item = self.get_item_by_id(item_id)

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
        item = self.get_item_by_id(item_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Quotation item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting quotation item with id '{item_id}': {e}")
            raise


    def get_all_items(self):
        try:
            return self.session.scalars(select(QuotationItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotation items: {e}")
            return []
