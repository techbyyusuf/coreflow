from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from models.models import Customer

class CustomerService:
    def __init__(self, session):
        self.session = session

    def create_customer(self, name, email):
        try:
            new_customer = Customer(name=name, email=email)                             #was mache ich hier mit Password
            self.session.add(new_customer)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            print(f"Customer '{name}' already exists.")
            raise

    def get_all_customers(self):
        try:
            return self.session.scalars(select(Customer)).all()
        except SQLAlchemyError as e:
            print(f"Error retrieving customers: {e}")
            return []
                                                                                        # update von anderen Daten?
    def update_customer_email(self, customer_id, new_email):
                                                                                        # e-mail checken
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if customer:
                customer.email = new_email
                self.session.commit()
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            print(f"Error updating movie: {e}")
            raise

    def delete_customer(self, customer_id):
        try:
            customer = self.session.scalars(select(Customer)).filter_by(id=customer_id).first()
            if customer:
                self.session.delete(customer)
                self.session.commit()

        except SQLAlchemyError:
            self.session.rollback()
            print(f"User with id '{customer_id}' does not exist.")
            raise