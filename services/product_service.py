import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.product import Product


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductService:
    """
    Service class for handling CRUD operations related to Product.
    """

    def __init__(self, session):
        """
        Initializes the ProductService with a database session.
        :param session: SQLAlchemy session object
        """
        self.session = session

    def create_product(self, user_id: int, name: str, unit_price: float, unit: int, description: str = None) -> None:
        """
        Creates a new product in the database.
        :param user_id: ID of the user who owns the product
        :param name: Product name
        :param unit_price: Unit price of the product
        :param unit: Unit count
        :param description: Optional description
        :raises SQLAlchemyError: If database error occurs
        """
        new_product = Product(
            user_id=user_id,
            name=name,
            unit_price=unit_price,
            unit=unit,
            description=description
        )

        try:
            self.session.add(new_product)
            self.session.commit()
            logger.info(f"Product '{name}' created successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating product '{name}': {e}")
            raise

    def get_all_products(self):
        """
        Retrieves all products from the database.
        :return: List of Product objects or empty list on error
        """
        try:
            return self.session.scalars(select(Product)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products: {e}")
            return []

    def update_product_price(self, product_id: int, new_price: float) -> None:
        """
        Updates the unit price of a product.
        :param product_id: ID of the product to update
        :param new_price: New unit price
        :raises ValueError: If product not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            product = self.session.scalars(select(Product)).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found.")

            product.unit_price = new_price
            self.session.commit()
            logger.info(f"Product price updated successfully for id {product_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating product price: {e}")
            raise

    def update_product_name(self, product_id: int, new_name: str) -> None:
        """
        Updates the name of a product.
        :param product_id: ID of the product to update
        :param new_name: New product name
        :raises ValueError: If product not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            product = self.session.scalars(select(Product)).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found.")

            product.name = new_name
            self.session.commit()
            logger.info(f"Product name updated successfully for id {product_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating product name: {e}")
            raise

    def update_product_description(self, product_id: int, new_description: str) -> None:
        """
        Updates the description of a product.
        :param product_id: ID of the product to update
        :param new_description: New product description
        :raises ValueError: If product not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            product = self.session.scalars(select(Product)).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found.")

            product.description = new_description
            self.session.commit()
            logger.info(f"Product description updated successfully for id {product_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating product description: {e}")
            raise

    def update_product_unit(self, product_id: int, new_unit: int) -> None:
        """
        Updates the unit count of a product.
        :param product_id: ID of the product to update
        :param new_unit: New unit value
        :raises ValueError: If product not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            product = self.session.scalars(select(Product)).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id {product_id} not found.")

            product.unit = new_unit
            self.session.commit()
            logger.info(f"Product unit updated successfully for id {product_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating product unit: {e}")
            raise

    def delete_product(self, product_id: int) -> None:
        """
        Deletes a product from the database.
        :param product_id: ID of the product to delete
        :raises ValueError: If product not found
        :raises SQLAlchemyError: If database error occurs
        """
        try:
            product = self.session.scalars(select(Product)).filter_by(id=product_id).first()
            if not product:
                raise ValueError(f"Product with id '{product_id}' does not exist.")

            self.session.delete(product)
            self.session.commit()
            logger.info(f"Product with id '{product_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting product with id '{product_id}': {e}")
            raise
