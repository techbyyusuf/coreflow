from models.models import Product

class ProductService:
    def __init__(self, session):
        self.session = session

    def create_product(self, name, price):
        new_product = Product(name=name, price=price)
        self.session.add(new_product)
        self.session.commit()

    def get_all_products(self):
        return self.session.query(Product).all()

    def update_product_price(self, product_id, new_price):
        product = self.session.query(Product).filter_by(id=product_id).first()
        if product:
            product.price = new_price
            self.session.commit()

    def delete_product(self, product_id):
        product = self.session.query(Product).filter_by(id=product_id).first()
        if product:
            self.session.delete(product)
            self.session.commit()
