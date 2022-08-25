from managers.base_manager import BaseManager
from models import CustomerDetailsModel


class CustomerDetailsManager(BaseManager):
    MODEL = CustomerDetailsModel
    UNIQUE = True
