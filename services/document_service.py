import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.document import Document
from models.enums import DocumentType, DocumentStatus, VALID_STATUSES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self, session):
        self.session = session

    def create_document(
        self,
        document_type: str,
        customer_id: int,
        user_id: int,
        issue_date,
        due_date=None,
        delivery_date=None,
        invoice_number=None,
        status: str = "OPEN",
        reference: str = None,
        notes: str = None
    ) -> None:
        if document_type.upper() not in DocumentType.__members__:
            raise ValueError(f"Invalid document type: {document_type}")

        doc_type_enum = DocumentType[document_type.upper()]

        if status.upper() not in DocumentStatus.__members__:
            raise ValueError(f"Invalid document status: {status}")

        allowed_statuses = VALID_STATUSES[doc_type_enum.name]
        if status.upper() not in allowed_statuses:
            raise ValueError(f"Status '{status}' is not allowed for document type '{doc_type_enum.value}'.")

        new_document = Document(
            document_type=doc_type_enum,
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date,
            delivery_date=delivery_date,
            invoice_number=invoice_number,
            status=DocumentStatus[status.upper()],
            reference=reference,
            notes=notes
        )

        try:
            self.session.add(new_document)
            self.session.commit()
            logger.info(f"Document created successfully for customer id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating document: {e}")
            raise

    def get_all_documents(self):
        try:
            return self.session.scalars(select(Document)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving documents: {e}")
            return []

    def get_document_by_id(self, document_id: int) -> Document | None:
        return self.session.scalars(select(Document).where(Document.id == document_id)).first()

    def update_document_status(self, document_id: int, new_status: str) -> None:
        if new_status.upper() not in DocumentStatus.__members__:
            raise ValueError(f"Invalid document status: {new_status}")

        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found.")

        allowed_statuses = VALID_STATUSES[document.document_type.name]
        if new_status.upper() not in allowed_statuses:
            raise ValueError(f"Status '{new_status}' is not allowed for document type '{document.document_type.value}'.")

        try:
            document.status = DocumentStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Document status updated successfully for id {document_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating document status: {e}")
            raise

    def update_document_reference(self, document_id: int, new_reference: str) -> None:
        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found.")

        try:
            document.reference = new_reference
            self.session.commit()
            logger.info(f"Document reference updated successfully for id {document_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating document reference: {e}")
            raise

    def update_document_notes(self, document_id: int, new_notes: str) -> None:
        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found.")

        try:
            document.notes = new_notes
            self.session.commit()
            logger.info(f"Document notes updated successfully for id {document_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating document notes: {e}")
            raise

    def delete_document(self, document_id: int) -> None:
        document = self.get_document_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id '{document_id}' does not exist.")

        try:
            self.session.delete(document)
            self.session.commit()
            logger.info(f"Document with id '{document_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting document with id '{document_id}': {e}")
            raise
