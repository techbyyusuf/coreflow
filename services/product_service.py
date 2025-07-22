import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.product import Product
from models.enums import UnitType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductService:
    """
    Service class for managing products including creation, updates, and deletion.
    """

    def __init__(self, session):
        """
        Initializes the service with a database session.
        """
        self.session = session


    def raise_if_product_name_exists(self, product_name: str) -> None:
        """
        Checks if a product name already exists and raises an error if it does.

        Args:
            product_name (str): Name to check.

        Raises:
            ValueError: If the product name is already in use.
        """
        stmt = select(Product).where(Product.name == product_name)
        product = self.session.scalars(stmt).first()

        if product:
            raise ValueError("Product name already in use by another product.")
        return None


    def get_product_by_id_or_raise(self, product_id: int) -> Product | None:
        """
        Retrieves a product by ID or raises an error if not found.

        Args:
            product_id (int): ID of the product.

        Returns:
            Product: The product instance.
        """
        stmt = select(Product).where(Product.id == product_id)
        product = self.session.scalars(stmt).first()

        if not product:
            raise ValueError(f"Product with id '{product_id}' not found.")
        return product


    def create_product(self, name: str, unit_price: float, unit: str, description: str = None) -> None:
        """
        Creates a new product after checking for duplicates and valid unit.

        Args:
            name (str): Product name.
            unit_price (float): Price per unit.
            unit (str): Unit of measurement.
            description (str, optional): Product description.

        Raises:
            ValueError: If input is invalid or duplicate.
        """
        if unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

        self.raise_if_product_name_exists(name)

        new_product = Product(
            name=name,
            unit_price=unit_price,
            unit=UnitType[unit.upper()],
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

        Returns:
            list: List of Product instances.
        """
        try:
            return self.session.scalars(select(Product)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products: {e}")
            return []


    def update_product_price(self, product_id: int, new_unit_price: float) -> None:
        """
        Updates the unit price of a product.

        Args:
            product_id (int): Product ID.
            new_unit_price (float): New unit price.

        Raises:
            ValueError: If price is negative.
        """
        product = self.get_product_by_id_or_raise(product_id)

        if new_unit_price < 0:
            raise ValueError("Unit price must be zero or positive.")

        try:
            product.unit_price = new_unit_price
            self.session.commit()
            logger.info(f"Product price updated successfully for id {product_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating product price: {e}")
            raise


    def update_product_name(self, product_id: int, new_name: str) -> None:
        """
        Updates the name of a product.

        Args:
            product_id (int): Product ID.
            new_name (str): New name.

        Raises:
            ValueError: If the name already exists.
        """
        product = self.get_product_by_id_or_raise(product_id)

        self.raise_if_product_name_exists(new_name)

        try:
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

        Args:
            product_id (int): Product ID.
            new_description (str): New description text.
        """
        product = self.get_product_by_id_or_raise(product_id)

        try:
            product.description = new_description
            self.session.commit()
            logger.info(f"Product description updated successfully for id {product_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating product description: {e}")
            raise


    def update_product_unit(self, product_id: int, new_unit: str) -> None:
        """
        Updates the unit of a product.

        Args:
            product_id (int): Product ID.
            new_unit (str): New unit value.

        Raises:
            ValueError: If the new unit is not valid.
        """
        product = self.get_product_by_id_or_raise(product_id)

        if new_unit.upper() not in UnitType.__members__:
            raise ValueError(f"Invalid unit: {new_unit}")

        try:
            product.unit = UnitType[new_unit.upper()]
            self.session.commit()
            logger.info(f"Product unit updated successfully for id {product_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating product unit: {e}")
            raise


    def delete_product(self, product_id: int) -> None:
        """
        Deletes a product by ID.

        Args:
            product_id (int): ID of the product to delete.
        """
        product = self.get_product_by_id_or_raise(product_id)

        try:
            self.session.delete(product)
            self.session.commit()
            logger.info(f"Product with id '{product_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting product with id '{product_id}': {e}")
            raise
