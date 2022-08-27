from werkzeug.exceptions import BadRequest

from db import db
from managers.base_manager import BaseManager
from managers.shop_manager import ShopManager
from models import ProductModel
from services.s3 import s3
from services.stripeService import StripeService
from utils.helpers import get_photo_name_by_url


class ProductManager(BaseManager):
    MODEL = ProductModel
    SHOP_ID_ERROR_MESSAGE = "Invalid shop id!"
    INACTIVE_SHOP_ERROR_MESSAGE = "Provided shops must be active if product is listed!"
    FOREIGN_SHOP_ERROR_MESSAGE = "Foreign shop provided!"

    def create(self, data, user, **kwargs):
        products = []
        try:
            for d in data:
                product = self.create_single_product(d, user, **kwargs)
                products.append(product)

            db.session.add_all(products)
            db.session.flush()
            return products

        except Exception as ex:
            for product in products:
                photo = get_photo_name_by_url(product.product_image_url)
                if photo:
                    s3.delete_photo(photo)
                if product.stripe_price_id:
                    StripeService.deactivate(product.stripe_price_id)
            raise ex

    def create_single_product(self, data, user, **kwargs):
        # Get shops
        shops_id = data.pop('shops_id')
        shops = ShopManager().get_shops_by_ids(shops_id)
        # if any of shops id is invalid
        if not len(shops_id) == len(shops):
            raise BadRequest(self.SHOP_ID_ERROR_MESSAGE)
        if [shop for shop in shops if shop and shop.holder_id != user.id]:
            raise BadRequest(self.FOREIGN_SHOP_ERROR_MESSAGE)

        # if there is inactive shops provided
        if data.get("listed") and [shop for shop in shops if shop and not shop.active]:
            raise BadRequest(self.INACTIVE_SHOP_ERROR_MESSAGE)

        # create product without save it in db
        product = super().create(data, user, add_to_db=False, **kwargs)
        try:
            [shop.products.append(product) for shop in shops]

            if product.listed:
                # create stripe price and product
                stripe_data = StripeService.create(product)
                product.stripe_price_id = stripe_data.get("price").get("id")
                product.stripe_product_id = stripe_data.get("product").get("id")
        except Exception as ex:
            photo = get_photo_name_by_url(product.product_image_url)
            if photo:
                s3.delete_photo(photo)
            if product.stripe_price_id:
                StripeService.deactivate(product.stripe_price_id)
            raise ex
        return product
