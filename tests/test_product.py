from models import ProductCategories
from tests.base_test_case import BaseTestCase
from tests.constants import Endpoints
from tests.factories import OwnerFactory
from tests.helpers import generate_token


class TestCreateProduct(BaseTestCase):
    URL = Endpoints.PRODUCT
    _count = 0

    @classmethod
    def _get_valid_data(cls, shops_id=None, listed=False):
        cls._count += 1
        if not shops_id:
            shops_id = []
        return {
            "name": f"TEST{cls._count}",
            "quantity": 20,
            "price": 100,
            "category": ProductCategories.pets.name,
            "shops_id": shops_id,
            "listed": listed,
        }

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    # def _create_owner_details_in_test_db(self, data=None):
    #     data = data if data else self.SHOP_OWNER_DETAILS_DATA
    #     details = ShopOwnerDetailsModel(holder_id=self._owner.id, **data)
    #     db.session.add(details)
    #     db.session.commit()
    #     return details

    def test_with_invalid_data_expect_400_and_correct_error_message(self):
        invalid_data = [
            {
                "name": "d",
                "quantity": -10,
                "price": -11,
                "category": "test",
                "shops_id": [1],
                "listed": True
            },
            {
                "name": "sdsa",
                "quantity": 1,
                "price": -11,
                "category": ProductCategories.pets.name,
                "shops_id": [],
                "listed": False
            },
        ]
        resp = self.client.post(self.URL, headers=self._create_authorization_header(OwnerFactory), json=invalid_data)

        self.assertEqual(400, resp.status_code)
        self.assertIn("name", resp.json["message"]["0"])
        self.assertIn("quantity", resp.json["message"]["0"])
        self.assertIn("price", resp.json["message"]["0"])
        self.assertIn("category", resp.json["message"]["0"])
        self.assertIn("price", resp.json["message"]["1"])

    def test_with_invalid_listed_with_no_shops_expect_400_and_correct_error_message(self):
        invalid_data = [
            {
                "name": "dds",
                "quantity": 0,
                "price": 1,
                "category": ProductCategories.pets.name,
                "shops_id": [],
                "listed": True
            },
            {
                "name": "sdsa",
                "quantity": 1,
                "price": 11,
                "category": ProductCategories.pets.name,
                "shops_id": [],
                "listed": False
            },
        ]
        resp = self.client.post(self.URL, headers=self._create_authorization_header(OwnerFactory), json=invalid_data)
        self.assertEqual(400, resp.status_code)
        self.assertIn("_schema", resp.json["message"]["0"])

    def test_with_valid_data_and_one_product_not_listed_no_shops_expect_201_correct_json_and_record_in_db(self):
        data = self._get_valid_data(shops_id=[], listed=False)
        resp = self.client.post(
            self.URL,
            headers=self._create_authorization_header(OwnerFactory),
            json=data)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(data["name"], resp.json["name"])
        self.assertEqual(data["quantity"], resp.json["quantity"])
        self.assertEqual(data["price"], resp.json["price"])
        self.assertListEqual(data["shops_id"], resp.json["in_shops"])
        self.assertEqual(data["listed"], resp.json["listed"])

    def test_with_valid_data_and_one_product_not_listed_has_shops_expect_201_correct_json_and_record_in_db(self):
        pass

    def test_with_valid_data_and_one_product_listed_has_shops_expect_201_correct_json_and_record_in_db(self):
        pass

    def test_with_valid_data_and_many_product_not_listed_no_shops_expect_201_correct_json_and_record_in_db(self):
        pass

    def test_with_valid_data_and_many_product_listed_shops_expect_201_correct_json_and_record_in_db(self):
        pass

    def test_with_valid_data_and_many_product_listed_no_shops_expect_400(self):
        pass
