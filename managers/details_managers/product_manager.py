from managers.base_manager import BaseManager
from models import ProductModel


class ProductManager(BaseManager):
    MODEL = ProductModel
