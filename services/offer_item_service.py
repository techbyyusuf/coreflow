import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.offer_item import OfferItem

logger = logging.getLogger(__name__)


class OfferItemService:
    """
    Service class for handling CRUD operations related to OfferItem.
    """

    def __init__(self, session):
        """
        Initializes the OfferItemService with a database session.

        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_offer_item(self, offer_id: int, product_id: int, quantity: int, unit_price: float) -> None:
        """
        Creates a new offer item.

        :param offer_id: ID of the offer
        :param product_id: ID of the product
        :param quantity: Quantity of the product
        :param unit_price: Price per unit
        :raises SQLAlchemyError: If database error occurs
        """
        new_offer_item = OfferItem(
            offer_id=offer_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        try:
            self.session.add(new_offer_item)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating offer item for offer {offer_id}: {e}")
            raise

    def get_all_offer_items(self):
        """
        Retrieves all offer items.

        :return: List of OfferItem objects or empty list on error
        """
        try:
            return self.session.scalars(select(OfferItem)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving offer items: {e}")
            return []

    def update_offer_item_quantity(self, item_id: int, new_quantity: int) -> None:
        """
        Updates the quantity of an offer item.

        :param item_id: ID of the offer item
        :param new_quantity: New quantity value
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(OfferItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Offer item with id '{item_id}' not found.")

            item.quantity = new_quantity
            self.session.commit()

        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating offer item quantity: {e}")
            raise

    def delete_offer_item(self, item_id: int) -> None:
        """
        Deletes an offer item.

        :param item_id: ID of the offer item
        :raises ValueError: If item not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            item = self.session.scalars(select(OfferItem)).filter_by(id=item_id).first()
            if not item:
                raise ValueError(f"Offer item with id '{item_id}' does not exist.")

            self.session.delete(item)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting offer item with id '{item_id}': {e}")
            raise
