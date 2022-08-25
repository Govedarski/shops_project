from flask_testing import TestCase

from config import create_app
from db import db
from tests.constants import TEST_CONFIGURATION


class BaseTestCase(TestCase):
    _HEADER_CONT_TYPE_JSON = {"Content-Type": "application/json"}

    def create_app(self):
        app = create_app(TEST_CONFIGURATION)

        @app.after_request
        def return_response(response):
            db.session.commit()
            return response

        return app

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
