from managers.base_manager import CRUDManager
from models import DeliveryAddressDetailsModel


class DeliveryAddressDetailsManager(CRUDManager):
    MODEL = DeliveryAddressDetailsModel
