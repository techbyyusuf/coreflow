import enum

"""
Defines enumeration types used across the application.

Includes:
    UserRole: Roles assigned to users (e.g., ADMIN, EMPLOYEE, VIEWER).
    UnitType: Measurement units for products (e.g., piece, kg, hour).
    OrderStatus: States an order can be in (e.g., draft, open, shipped).
    QuotationStatus: States a quotation can be in (e.g., sent, accepted, expired).
    InvoiceStatus: States an invoice can be in (e.g., paid, overdue, cancelled).
"""


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    VIEWER = "VIEWER"


class UnitType(enum.Enum):
    PIECE = "Stück"
    KILOGRAM = "kg"
    HOUR = "h"


class OrderStatus(enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    OPEN = "open"
    COMPLETED = "completed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


class QuotationStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"


class InvoiceStatus(enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
