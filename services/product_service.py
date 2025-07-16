import logging
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.product import Product
from models.enums import UnitType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, session):
        self.session = session

    def create_product(self, name: str, unit_price: float, unit: str, description: str = None) -> None:
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
        try:
            return self.session.scalars(select(Product)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving products: {e}")
            return []

    def get_product_by_id(self, product_id: int) -> Product | None:
        return self.session.scalars(
            select(Product).where(Product.id == product_id)
        ).first()

    def update_product_price(self, product_id: int, new_price: float) -> None:
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found.")

        try:
            product.unit_price = new_price
            self.session.commit()
            logger.info(f"Product price updated successfully for id {product_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating product price: {e}")
            raise

    def update_product_name(self, product_id: int, new_name: str) -> None:
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found.")

        existing_product = self.session.scalars(
            select(Product).where(Product.name == new_name)
        ).first()
        if existing_product and existing_product.id != product_id:
            raise ValueError("Product name already in use by another product.")

        try:
            product.name = new_name
            self.session.commit()
            logger.info(f"Product name updated successfully for id {product_id}.")
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            logger.error(f"Error updating product name: {e}")
            raise

    def update_product_description(self, product_id: int, new_description: str) -> None:
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found.")

        try:
            product.description = new_description
            self.session.commit()
            logger.info(f"Product description updated successfully for id {product_id}.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating product description: {e}")
            raise

    def update_product_unit(self, product_id: int, new_unit: str) -> None:
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found.")

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
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id '{product_id}' does not exist.")

        try:
            self.session.delete(product)
            self.session.commit()
            logger.info(f"Product with id '{product_id}' deleted successfully.")
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error deleting product with id '{product_id}': {e}")
            raise
