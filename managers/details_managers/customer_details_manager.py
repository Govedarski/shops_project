from managers.base_manager import CRUDManager
from models import CustomerDetailsModel


class CustomerDetailsManager(CRUDManager):
    MODEL = CustomerDetailsModel
    UNIQUE = True
