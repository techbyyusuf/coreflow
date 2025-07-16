import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseItemService:
    def __init__(self, session, item_model, document_model, document_id_field: str):
        """
        :param session: SQLAlchemy session
        :param item_model: Das Item-Modell (z. B. OrderItem)
        :param document_model: Das Dokument-Modell (z. B. Order)
        :param document_id_field: Name des Foreign-Key-Feldes (z. B. "order_id", "quotation_id")
        """
        self.session = session
        self.item_model = item_model
        self.document_model = document_model
        self.document_id_field = document_id_field

    def get_document_by_id(self, document_id: int):
        return self.session.scalars(
            select(self.document_model).where(self.document_model.id == document_id)
        ).first()

    def get_item_by_id(self, item_id: int):
        return self.session.scalars(
            select(self.item_model).where(self.item_model.id == item_id)
        ).first()

    def create_item(self, document_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found.")

        kwargs = {
            self.document_id_field: document_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price
        }

        new_item = self.item_model(**kwargs)

        try:
            self.session.add(new_item)
            self.session.commit()
            logger.info(f"Item created successfully for {self.document_id_field}={document_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating item: {e}")
            raise

    def update_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found.")

        try:
            item.quantity = new_quantity
            item.unit_price = new_unit_price
            self.session.commit()
            logger.info(f"Item updated successfully for id {item_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating item: {e}")
            raise

    def delete_item(self, item_id: int) -> None:
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id '{item_id}' does not exist.")

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting item with id '{item_id}': {e}")
            raise

    def get_all_items(self):
        try:
            return self.session.scalars(select(self.item_model)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving items: {e}")
            return []
