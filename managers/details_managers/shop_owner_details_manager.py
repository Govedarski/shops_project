from managers.base_manager import CRUDManager
from models import ShopOwnerDetailsModel


class ShopOwnerDetailsManager(CRUDManager):
    MODEL = ShopOwnerDetailsModel
    UNIQUE = True
