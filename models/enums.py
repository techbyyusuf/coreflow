import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"
    VIEWER = "viewer"


class UnitType(enum.Enum):
    PIECE = "Stück"
    KILOGRAM = "kg"
    HOUR = "h"


class DocumentType(enum.Enum):
    ORDER = "order"
    INVOICE = "invoice"


class DocumentStatus(enum.Enum):
    OPEN = "open"
    PAID = "paid"
    SHIPPED = "shipped"
    CLOSE = "closed"
