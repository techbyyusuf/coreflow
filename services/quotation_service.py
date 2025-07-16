import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.quotation import Quotation
from models.enums import QuotationStatus
from models.customer import Customer
from models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuotationService:
    def __init__(self, session):
        self.session = session

    def get_quotation_by_id_or_raise(self, quotation_id: int) -> Quotation | None:
        stmt = select(Quotation).where(Quotation.id == quotation_id)
        quotation =  self.session.scalars(stmt).first()

        if not quotation:
            raise ValueError(f"Quotation with id {quotation_id} not found.")
        return quotation


    def get_customer_or_raise(self, customer_id: int) -> Customer:
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = self.session.scalars(stmt).first()

        if not customer:
            raise ValueError(f"Customer with id {customer_id} not found.")
        return customer


    def get_user_or_raise(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        user = self.session.scalars(stmt).first()

        if not user:
            raise ValueError(f"User with id {user_id} not found.")
        return user
    

    def create_quotation(
        self,
        customer_id: int,
        user_id: int,
        issue_date,
        due_date=None,
        quotation_number: str = None,
        status: str = "DRAFT",
        notes: str = None
    ) -> None:
        self.get_customer_or_raise(customer_id)
        self.get_user_or_raise(user_id)
        
        if quotation_number is not None:
            existing_quotation = self.session.scalars(
                select(Quotation).where(Quotation.quotation_number == quotation_number)
            ).first()
            if existing_quotation:
                raise ValueError("Quotation number already in use.")

        if status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid quotation status: {status}")

        new_quotation = Quotation(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            due_date=due_date,
            quotation_number=quotation_number,
            status=QuotationStatus[status.upper()],
            notes=notes
        )

        try:
            self.session.add(new_quotation)
            self.session.commit()
            logger.info(f"Quotation created successfully for customer id {customer_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating quotation: {e}")
            raise

    def get_all_quotations(self):
        try:
            return self.session.scalars(select(Quotation)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotations: {e}")
            return []

    def update_quotation_status(self, quotation_id: int, new_status: str) -> None:
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        if new_status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid quotation status: {new_status}")

        try:
            quotation.status = QuotationStatus[new_status.upper()]
            self.session.commit()
            logger.info(f"Quotation status updated successfully for id {quotation_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating quotation status: {e}")
            raise

    def update_quotation_notes(self, quotation_id: int, new_notes: str) -> None:
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        try:
            quotation.notes = new_notes
            self.session.commit()
            logger.info(f"Quotation notes updated successfully for id {quotation_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating quotation notes: {e}")
            raise

    def delete_quotation(self, quotation_id: int) -> None:
        quotation = self.get_quotation_by_id_or_raise(quotation_id)

        try:
            self.session.delete(quotation)
            self.session.commit()
            logger.info(f"Quotation with id '{quotation_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting quotation with id '{quotation_id}': {e}")
            raise


    def get_quotations_by_status(self, status: str):
        if status.upper() not in QuotationStatus.__members__:
            raise ValueError(f"Invalid invoice status: {status}")

        try:
            return self.session.scalars(
                select(Quotation).where(Quotation.status == QuotationStatus[status.upper()])
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving quotations with status '{status}': {e}")
            return []
