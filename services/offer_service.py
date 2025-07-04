import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.offer import Offer

logger = logging.getLogger(__name__)


class OfferService:
    """
    Service class for handling CRUD operations related to Offer.
    """

    def __init__(self, session):
        """
        Initializes the OfferService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_offer(self, customer_id: int, user_id: int, issue_date, valid_until,
                     status: str, notes: str = None) -> None:
        """
        Creates a new offer in the database.

        :param customer_id: ID of the customer
        :param user_id: ID of the user
        :param issue_date: Date when the offer was issued
        :param valid_until: Date until which the offer is valid
        :param status: Status of the offer (e.g., "pending", "accepted")
        :param notes: Optional notes
        :raises SQLAlchemyError: If database error occurs
        """
        new_offer = Offer(
            customer_id=customer_id,
            user_id=user_id,
            issue_date=issue_date,
            valid_until=valid_until,
            status=status,
            notes=notes
        )

        try:
            self.session.add(new_offer)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating offer for customer {customer_id}: {e}")
            raise

    def get_all_offers(self):
        """
        Retrieves all offers from the database.

        :return: List of Offer objects or empty list on error
        """
        try:
            return self.session.scalars(select(Offer)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving offers: {e}")
            return []

    def update_offer_status(self, offer_id: int, new_status: str) -> None:
        """
        Updates the status of an offer.

        :param offer_id: ID of the offer to update
        :param new_status: New status value
        :raises ValueError: If offer not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            offer = self.session.scalars(select(Offer)).filter_by(id=offer_id).first()
            if not offer:
                raise ValueError(f"Offer with id '{offer_id}' not found.")

            offer.status = new_status
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating offer status: {e}")
            raise

    def delete_offer(self, offer_id: int) -> None:
        """
        Deletes an offer from the database.

        :param offer_id: ID of the offer to delete
        :raises ValueError: If offer not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            offer = self.session.scalars(select(Offer)).filter_by(id=offer_id).first()
            if not offer:
                raise ValueError(f"Offer with id '{offer_id}' does not exist.")

            self.session.delete(offer)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting offer with id '{offer_id}': {e}")
            raise
