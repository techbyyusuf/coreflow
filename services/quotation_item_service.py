from models.quotation import Quotation
from models.quotation_item import QuotationItem
from services.base_item_services import BaseItemService

class QuotationItemService(BaseItemService):
    def __init__(self, session):
        super().__init__(session, QuotationItem, Quotation)
