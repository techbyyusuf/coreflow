import enum

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
