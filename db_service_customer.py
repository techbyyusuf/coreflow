from models.models import Customer

class CustomerService:
    def __init__(self, session):
        self.session = session

    def create_customer(self, name, email):
        new_customer = Customer(name=name, email=email)
        self.session.add(new_customer)
        self.session.commit()

    def get_all_customers(self):
        return self.session.query(Customer).all()

    def update_customer_email(self, customer_id, new_email):
        customer = self.session.query(Customer).filter_by(id=customer_id).first()
        if customer:
            customer.email = new_email
            self.session.commit()

    def delete_customer(self, customer_id):
        customer = self.session.query(Customer).filter_by(id=customer_id).first()
        if customer:
            self.session.delete(customer)
            self.session.commit()
