from flask import request
from flask_restful import Resource

from services.stripeService import StripeService


class WebhookResource(Resource):
    def post(self, **kwargs):
        payload = request.get_data()
        sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')

        session = StripeService.webhook(payload, sig_header)
        p = 1
        return {}
