import stripe
from decouple import config
from werkzeug.exceptions import InternalServerError

stripe.api_key = config('STRIPE_SECRET_KEY')


class StripeService:
    PUBLIC_KEY = config('STRIPE_PUBLIC_KEY')

    @classmethod
    def create(cls, product):
        stripe_product_response = cls.create_product(product)
        stripe_price_response = cls.create_price(product, stripe_product_response.get('id'))
        return {
            "product": stripe_product_response,
            "price": stripe_price_response}

    @classmethod
    def create_product(cls, product):
        return stripe.Product.create(
            **cls._get_product_data(product)
        )

    @classmethod
    def create_price(cls, product, stripe_product_id):
        return stripe.Price.create(
            product=stripe_product_id,
            **cls._get_price_data(product)
        )

    @classmethod
    def update(cls, product, stripe_product_id, stripe_price_id):
        stripe_price_response = cls.update_price(product, stripe_price_id)
        new_stripe_price_id = stripe_price_response.get('id')

        stripe_product_response = cls.update_product(product, stripe_product_id, new_stripe_price_id)
        return {
            "product": stripe_product_response,
            "price": stripe_price_response}

    @classmethod
    def update_product(cls, product, stripe_product_id, stripe_price_id):
        return stripe.Product.modify(
            stripe_product_id,
            **cls._get_product_data(product),
        )

    @classmethod
    def update_price(cls, product, old_price_id):
        old_price_data = cls.retrieve_price(old_price_id)

        if not old_price_data.get("unit_amount") == cls._get_unit_amount(product.price):
            new_price_data = cls.create_price(product, old_price_data.get("product"))
            cls.deactivate(old_price_id)
            return new_price_data

        if not old_price_data.get("active") == cls._is_active(product):
            return stripe.Price.modify(
                old_price_id,
                active=cls._is_active(product),
            )

        return old_price_data

    @staticmethod
    def create_payment_link(price_data, success, cancel):
        try:
            return stripe.checkout.Session.create(
                success_url=success,
                cancel_url=cancel,
                line_items=price_data,
                mode="payment",
            )
        except Exception as ex:
            raise InternalServerError("Payment is temporarily unavailable!")

    @staticmethod
    def retrieve_price(price_id):
        return stripe.Price.retrieve(price_id)

    @staticmethod
    def deactivate(price_id):
        stripe.Price.modify(
            price_id,
            active=False,
        )

    @classmethod
    def _get_price_data(cls, product):
        return {"unit_amount": cls._get_unit_amount(product.price),
                "currency": "bgn",
                "active": cls._is_active(product),
                }

    @classmethod
    def _get_product_data(cls, product):
        return {"name": product.name,
                "description": product.description,
                "active": cls._is_active(product),
                "images": [product.product_image_url]
                }

    @staticmethod
    def _get_unit_amount(price):
        return int(price * 100)

    @staticmethod
    def _is_active(product):
        return product.quantity > 0

#
# if __name__ == '__main__':
#     class Product:
#         name = "test"
#         price = 54
#         quantity = 4
#         description = None
#         product_image_url = None
#
#
#     class MProduct:
#         name = "Mofidy test"
#         price = 20
#         quantity = 1
#         description = "Some description"
#         product_image_url = "https://hbr.org/resources/images/article_assets/2019/11/Nov19_14_sb10067951dd-001.jpg"
#
#
#     success_url = "https://example.com/success"
#     cancel_url = "https://example.com/cancel"
#     prod = Product()
#     mprod = MProduct()
#     r = StripeService.create(prod)
#     data = [{
#         "price": r.get("price").get("id"),
#         "quantity": 2,
#     }, ]
#
#     link = StripeService.create_payment_link(data, success_url, cancel_url)
#     # print(link)
#
#     mr = StripeService.update(mprod, r.get("product").get("id"), r.get("price").get("id"))
#
#     print(mr)
#
#     new_data = [{
#         "price": mr.get("price").get("id"),
#         "quantity": 2,
#     }, ]
#
#     link = StripeService.create_payment_link(new_data, success_url, cancel_url)
#     print(link)
