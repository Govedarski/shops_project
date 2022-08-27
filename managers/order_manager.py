from werkzeug.exceptions import BadRequest

from db import db
from managers.product_manager import ProductManager
from models.enums import PaymentMethod
from models.order_model import OrderModel, OrderProductModel
from services.stripeService import StripeService


class OrderManager:
    MODEL = OrderModel
    INVALID_PRODUCT_ID_MESSAGE = 'Invalid Product ID!'

    def create(self, data, *args, **kwargs):
        product_data = data.pop('products')
        order = self._create_order(data)
        self._create_order_details(order, product_data)
        payment_link = ""
        if order.payment_method == PaymentMethod.online:
            price_data = [
                {"price": product.product.stripe_price_id, "quantity": product.order_quantity}
                for product in order.products]
            payment_link = StripeService.create_payment_link(price_data).url
        return order, payment_link

    @staticmethod
    def _create_order(data):
        order = OrderModel(**data)
        db.session.add(order)
        db.session.flush()
        return order

    @classmethod
    def _create_order_details(cls, order, product_data):
        product_ids = [data.get('id') for data in product_data]
        products = db.session.query(ProductManager.get_model()) \
            .filter(ProductManager.get_model().id.in_(product_ids)) \
            .all()

        if not len(product_ids) == len(products):
            BadRequest(cls.INVALID_PRODUCT_ID_MESSAGE)
        total_price = 0
        for data in product_data:
            current_product = [product for product in products if product.id == data.get('id')][0]
            if current_product.quantity < data.get('quantity'):
                raise BadRequest(f'Product {current_product.name} out of stock')
            current_product.quantity -= data.get('quantity')

            price = current_product.price
            total_price += price
            order_product_data = OrderProductModel(
                order_id=order.id,
                product_id=data.get('id'),
                order_quantity=data.get('quantity'),
                order_price=price,
            )

            db.session.add(order_product_data)
        order.total_price = total_price
        db.session.flush()

    @classmethod
    def get_model(cls):
        return cls.MODEL
