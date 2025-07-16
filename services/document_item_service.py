import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.document_item import DocumentItem
from models.document import Document
from models.enums import DocumentStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentItemService:
    def __init__(self, session):
        self.session = session

    def get_document_by_id(self, document_id: int) -> Document | None:
        """
        Retrieves a single document by ID.
        """
        return self.session.scalars(select(Document).filter_by(id=document_id)).first()

    def get_open_document_or_raise(self, document_id: int) -> Document:
        """
        Retrieves the document and ensures it is in OPEN status.
        Raises ValueError if not found or not open.
        """
        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found.")
        if document.status != DocumentStatus.OPEN:
            raise ValueError(f"Document with id {document_id} is not open and cannot be modified.")
        return document

    def create_document_item(self, document_id: int, product_id: int, quantity: float, unit_price: float) -> None:
        """
        Creates a new document item for a given document.
        """
        self.get_open_document_or_raise(document_id)

        new_item = DocumentItem(
            document_id=document_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_item)
            self.session.commit()
            logger.info(f"Document item created successfully for document id {document_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating document item: {e}")
            raise

    def get_all_items(self):
        try:
            return self.session.scalars(select(DocumentItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving document items: {e}")
            return []

    def get_item_by_id(self, item_id: int) -> DocumentItem | None:
        return self.session.scalars(select(DocumentItem).filter_by(id=item_id)).first()

    def update_document_item(self, item_id: int, new_quantity: float, new_unit_price: float) -> None:
        """
        Updates quantity and unit price of a document item.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Document item with id {item_id} not found.")

        self.get_open_document_or_raise(item.document_id)

        try:
            item.quantity = new_quantity
            item.unit_price = new_unit_price
            self.session.commit()
            logger.info(f"Document item updated successfully for id {item_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating document item: {e}")
            raise

    def delete_document_item(self, item_id: int) -> None:
        """
        Deletes a document item.
        """
        item = self.get_item_by_id(item_id)
        if not item:
            raise ValueError(f"Document item with id '{item_id}' does not exist.")

        self.get_open_document_or_raise(item.document_id)

        try:
            self.session.delete(item)
            self.session.commit()
            logger.info(f"Document item with id '{item_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting document item with id '{item_id}': {e}")
            raise
