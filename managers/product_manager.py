from db import db
from managers.base_manager import BaseManager
from models import ProductModel, ShopModel


class ProductManager(BaseManager):
    MODEL = ProductModel

    def create(self, data, user, **kwargs):
        if isinstance(data, dict):
            shops_id = data.pop('shops_id')
            product = super().create(data, user, **kwargs)
            [ShopModel.query.filter_by(id=shop_id).first().products.append(product) for shop_id in shops_id]
            return product

        products = []
        photo_urls = []
        try:
            for product_data in products:
                product = super().create(product_data, user, add=False, **kwargs)
                products.append(product)
                photo_urls.append(product.product_image_url)

            db.session.add_all(products)
            db.session.flush()
        except Exception as ex:
            [self._delete_with_photos(self.get_model(), product) for product in products if product.image_url]
            raise ex
