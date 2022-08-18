from flask_testing import TestCase

from config import create_app
from db import db
from tests.constants import TEST_CONFIGURATION


class BaseTestCase(TestCase):
    _HEADER_CONT_TYPE_JSON = {"Content-Type": "application/json"}

    def create_app(self):
        return create_app(TEST_CONFIGURATION)

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
