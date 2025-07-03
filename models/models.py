from sqlalchemy import String, Float, Date, TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[int] = mapped_column()
    address: Mapped[str] = mapped_column(String, unique=True)
    tax_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    unit_price: Mapped[float] = mapped_column(Float)
    unit: Mapped[int] = mapped_column()
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column()
    issue_date: Mapped[Date] = mapped_column(Date)
    valid_until: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(String, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column()
    issue_date: Mapped[Date] = mapped_column(Date)
    delivery_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(String, nullable=True)


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column()
    invoice_number: Mapped[int] = mapped_column(unique=True)
    issue_date: Mapped[Date] = mapped_column(Date)
    due_date: Mapped[Date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String)
    referee: Mapped[str] = mapped_column(String)
    notes: Mapped[str] = mapped_column(String, nullable=True)


class OfferItem(Base):
    __tablename__ = "offeritems"

    id: Mapped[int] = mapped_column(primary_key=True)
    offer_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)


class OrderItem(Base):
    __tablename__ = "orderitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)


class InvoiceItem(Base):
    __tablename__ = "invoiceitems"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column()
    product_id: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(Float)
