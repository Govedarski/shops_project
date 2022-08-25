from models import ProductCategories
from tests.base_test_case import BaseTestCase
from tests.constants import Endpoints
from tests.factories import OwnerFactory
from tests.helpers import generate_token


class TestCreateProduct(BaseTestCase):
    URL = Endpoints.PRODUCT

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def test_with_invalid_data_expect_400_and_correct_error_message(self):
        invalid_data = [
            {
                "name": "ss",
                "quantity": 0,
                "price": -1,
                "category": ProductCategories.pets.name,
                "shops_id": [1],
                "listed": True
            },
            {
                "name": "sdsa",
                "quantity": 1,
                "price": 1,
                "category": ProductCategories.pets.name,
                "shops_id": [1],
                "listed": True
            },
        ]
        resp = self.client.post(self.URL, headers=self._create_authorization_header(OwnerFactory), json=invalid_data)
        print(resp.json)
