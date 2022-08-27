from sqlalchemy.exc import InvalidRequestError
from werkzeug.exceptions import BadRequest

from db import db
from managers.base_manager import BaseManager
from managers.shop_manager import ShopManager
from models import ProductModel, UserRoles
from services.s3 import s3
from services.stripeService import StripeService
from utils import helpers
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

    def get_list(self, criteria, **kwargs):

        user = kwargs.get('user')
        try:
            p = self._fetch_data(self.get_model(), criteria, user)
            return p
        except InvalidRequestError:
            # not sure empty list or BadRequest
            return []

    @staticmethod
    def _fetch_data(model, criteria, user):
        filtered_query = model.query
        if criteria.get("shop_ids"):
            shop_ids_list = [int(id_) for id_ in criteria.pop("shop_ids").split("-")]
            filtered_query = db.session.query(model).filter(
                model.in_shops.any(ShopManager.get_model().id.in_(shop_ids_list))
            )
        # if not auth user or customer return products by criteria which are listed
        if not user or user.role == UserRoles.customer:
            criteria = criteria | {"listed": True}
            return filtered_query.filter_by(**criteria).all()

        # if admin return all products by criteria
        if helpers.is_admin(user):
            return filtered_query.filter_by(**criteria).all()

        # if user want his own products
        if criteria.get('holder_id') == str(user.id):
            return model.query.filter_by(**criteria).all()

        # if user want all products fetch his products and all the rest which are listed
        if not criteria.get('holder_id'):
            user_shops = []
            if not criteria.get('listed'):
                holder_criteria = criteria | {"holder_id": user.id, "listed": False}
                user_shops = filtered_query.filter_by(**holder_criteria).all()

            foreign_criteria = criteria | {"listed": True}
            foreign_shops = filtered_query.filter_by(**foreign_criteria).all()
            return user_shops + foreign_shops

        # if user want someone else products fetch products by criteria which are listed
        if not criteria.get('holder_id') == str(user.id):
            foreign_criteria = criteria | {"listed": True}
            return filtered_query.filter_by(**foreign_criteria).all()
