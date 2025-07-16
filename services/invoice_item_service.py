from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from services.base_item_services import BaseItemService

class InvoiceItemService(BaseItemService):
    def __init__(self, session):
        super().__init__(session, InvoiceItem, Invoice)
