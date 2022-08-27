from unittest.mock import patch

from managers.product_manager import ProductManager
from models import ProductCategories, ProductModel
from services.stripeService import StripeService
from tests import helpers as test_helpers
from tests.base_test_case import BaseTestCase
from tests.constants import Endpoints
from tests.factories import OwnerFactory, ShopFactory
from tests.helpers import generate_token


class TestCreateProduct(BaseTestCase):
    URL = Endpoints.PRODUCT
    _count = 0

    def setUp(self):
        super().setUp()
        self.shop_owner = OwnerFactory()
        self.shops = [ShopFactory(active=True, holder_id=self.shop_owner.id) for _ in range(3)]
        self.shop_ids = [shop.id for shop in self.shops]
        token = generate_token(self.shop_owner)
        self.authorization_headers = {"Authorization": f"Bearer {token}"}

    @classmethod
    def _get_valid_data(cls, shop_ids=None, listed=False):
        cls._count += 1
        if not shop_ids:
            shop_ids = []
        return {
            "name": f"TEST{cls._count}",
            "quantity": 20,
            "price": 100,
            "category": ProductCategories.pets.name,
            "shops_id": shop_ids,
            "listed": listed,
        }

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def test_with_valid_data_and_one_product_not_listed_no_shops_expect_201_correct_json_and_record_in_db(self):
        data = self._get_valid_data()

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])
        product = ProductModel.query.first()

        self.assertEqual(201, resp.status_code)
        self.assertEqual(data["name"], resp.json[0]["name"])
        self.assertEqual(data["quantity"], resp.json[0]["quantity"])
        self.assertEqual(data["price"], resp.json[0]["price"])
        self.assertListEqual([], resp.json[0]["in_shops"])
        self.assertEqual(data["listed"], resp.json[0]["listed"])
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)
        self.assertListEqual(data["shops_id"], product.in_shops)
        self.assertEqual(data["listed"], product.listed)
        self.assertIsNone(product.stripe_product_id)
        self.assertIsNone(product.stripe_price_id)

    @patch.object(StripeService, "create", return_value={
        "product": {id: "some_stripe_product_id"},
        "price": {id: "some_stripe_product_id"}})
    def test_with_valid_data_one_product_listed_and_shops_expect_201_correct_json_and_record_in_db_and_stripe_ids(self,
                                                                                                                  mocked_stripe):
        data = self._get_valid_data(listed=True, shop_ids=self.shop_ids)

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        product = ProductModel.query.first()
        result_shop_ids = [shop.id for shop in product.in_shops]

        self.assertEqual(201, resp.status_code)
        self.assertEqual(data["name"], resp.json[0]["name"])
        self.assertEqual(data["quantity"], resp.json[0]["quantity"])
        self.assertEqual(data["price"], resp.json[0]["price"])
        self.assertEqual(3, len(resp.json[0]["in_shops"]))
        self.assertEqual(self.shops[0].id, resp.json[0]["in_shops"][0]["id"])
        self.assertEqual(self.shops[1].id, resp.json[0]["in_shops"][1]["id"])
        self.assertEqual(self.shops[2].id, resp.json[0]["in_shops"][2]["id"])
        self.assertEqual(data["listed"], resp.json[0]["listed"])
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(3, len(product.in_shops))
        self.assertIn(self.shops[0].id, result_shop_ids)
        self.assertIn(self.shops[1].id, result_shop_ids)
        self.assertIn(self.shops[2].id, result_shop_ids)
        self.assertEqual(data["listed"], product.listed)
        self.assertEqual(mocked_stripe.return_value.get("product").get("id"), product.stripe_product_id)
        self.assertEqual(mocked_stripe.return_value.get("price").get("id"), product.stripe_price_id)

    def test_with_valid_data_and_one_product_not_listed_has_shops_expect_201_correct_json_and_record_in_db(self):
        data = self._get_valid_data(listed=False, shop_ids=self.shop_ids)

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        product = ProductModel.query.first()
        result_shop_ids = [shop.id for shop in product.in_shops]

        self.assertEqual(201, resp.status_code)
        self.assertEqual(data["name"], resp.json[0]["name"])
        self.assertEqual(data["quantity"], resp.json[0]["quantity"])
        self.assertEqual(data["price"], resp.json[0]["price"])
        self.assertEqual(3, len(resp.json[0]["in_shops"]))
        self.assertEqual(self.shops[0].id, resp.json[0]["in_shops"][0]["id"])
        self.assertEqual(self.shops[1].id, resp.json[0]["in_shops"][1]["id"])
        self.assertEqual(self.shops[2].id, resp.json[0]["in_shops"][2]["id"])
        self.assertEqual(data["listed"], resp.json[0]["listed"])
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["quantity"], product.quantity)
        self.assertEqual(data["price"], product.price)
        self.assertEqual(3, len(product.in_shops))
        self.assertIn(self.shops[0].id, result_shop_ids)
        self.assertIn(self.shops[1].id, result_shop_ids)
        self.assertIn(self.shops[2].id, result_shop_ids)
        self.assertEqual(data["listed"], product.listed)
        self.assertIsNone(product.stripe_product_id)
        self.assertIsNone(product.stripe_price_id)

    def test_with_valid_data_and_one_product_not_listed_inactive_shop_id_expect_201_and_record_in_db(self):
        inactive_shop = ShopFactory(active=False, holder_id=self.shop_owner.id)
        shop_ids = self.shop_ids.copy()
        shop_ids.append(inactive_shop.id)
        data = self._get_valid_data(listed=False, shop_ids=shop_ids)

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        self.assertEqual(201, resp.status_code)
        test_helpers.assert_count_equal(1, ProductModel)

    def test_with_valid_data_and_one_product_listed_no_shops_expect_400_and_no_record_in_db(self):
        data = self._get_valid_data(listed=True)

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)

    def test_with_valid_data_and_one_product_not_listed_invalid_shop_id_expect_400_and_no_record_in_db(self):
        data = self._get_valid_data(listed=False, shop_ids=[231])

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)
        self.assertEqual(ProductManager.SHOP_ID_ERROR_MESSAGE, resp.json["message"])

    def test_with_valid_data_and_one_product_listed_inactive_shop_id_expect_400_and_no_record_in_db(self):
        inactive_shop = ShopFactory(active=False, holder_id=self.shop_owner.id)
        shop_ids = self.shop_ids.copy()
        shop_ids.append(inactive_shop.id)
        data = self._get_valid_data(listed=True, shop_ids=shop_ids)

        resp = self.client.post(
            self.URL,
            headers=self.authorization_headers,
            json=[data])

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)
        self.assertEqual(ProductManager.INACTIVE_SHOP_ERROR_MESSAGE, resp.json["message"])

    def test_with_one_product_not_listed_foreign_shop_id_expect_400_and_no_record_in_db(self):
        data = self._get_valid_data(listed=False, shop_ids=self.shop_ids)

        resp = self.client.post(
            self.URL,
            headers=self._create_authorization_header(OwnerFactory),
            json=[data])

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)
        self.assertEqual(ProductManager.FOREIGN_SHOP_ERROR_MESSAGE, resp.json["message"])

    def test_with_valid_data_and_many_products_expect_201_correct_json_and_record_in_db(self):
        data = [self._get_valid_data() for _ in range(5)]

        resp = self.client.post(
            self.URL,
            headers=self._create_authorization_header(OwnerFactory),
            json=data)

        self.assertEqual(201, resp.status_code)
        test_helpers.assert_count_equal(5, ProductModel)

    def test_with_invalid_data_and_many_products_expect_400_and_no_record_in_db(self):
        data = [self._get_valid_data() for _ in range(5)]

        resp = self.client.post(
            self.URL,
            headers=self._create_authorization_header(OwnerFactory),
            json=[data])

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)
        self.assertEqual(ProductManager.FOREIGN_SHOP_ERROR_MESSAGE, resp.json["message"])

    def test_with_valid_data_and_many_products_and_one_invalid_expect_400_and_no_record_in_db(self):
        data = [self._get_valid_data() for _ in range(5)]
        invalid_data = self._get_valid_data(shop_ids=[964])
        data.append(invalid_data)

        resp = self.client.post(
            self.URL,
            headers=self._create_authorization_header(OwnerFactory),
            json=data)

        self.assertEqual(400, resp.status_code)
        test_helpers.assert_count_equal(0, ProductModel)
