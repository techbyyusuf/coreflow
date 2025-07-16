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
    OFFER = "offer"


class DocumentStatus(enum.Enum):
    PAID = "paid"
    SHIPPED = "shipped"
    DRAFT = "draft"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"


VALID_STATUSES = {
    "ORDER": {"DRAFT", "OPEN", "PROCESSING", "COMPLETED", "SHIPPED", "CANCELLED"},
    "OFFER": {"DRAFT", "SENT", "ACCEPTED", "REJECTED", "EXPIRED"},
    "INVOICE": {"DRAFT", "OPEN", "SENT", "PAID", "OVERDUE"}
}

