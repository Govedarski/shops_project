from db import db
from tests.base_test_case import BaseTestCase
from tests.constants import Endpoints
from tests.factories import OwnerFactory, ShopFactory, ProductFactory, CustomerFactory, AdminFactory
from tests.helpers import generate_token


class TessGetListProducts(BaseTestCase):
    URL = Endpoints.PRODUCT
    _count = 0

    def setUp(self):
        super().setUp()
        self.shop_owner = OwnerFactory()
        self.shops = [ShopFactory(active=True, holder_id=self.shop_owner.id) for _ in range(3)]
        self.shop_ids = [shop.id for shop in self.shops]
        token = generate_token(self.shop_owner)
        self.authorization_headers = {"Authorization": f"Bearer {token}"}
        self.products = [ProductFactory(holder_id=self.shop_owner.id, listed=True) for _ in range(3)]

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def test_with_listed_products_user_holder_expect_200_and_correct_json(self):
        resp = self.client.get(
            self.URL,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json))
        self.assertEqual(self.products[0].name, resp.json[0]["name"])
        self.assertEqual(self.products[0].quantity, resp.json[0]["quantity"])
        self.assertEqual(self.products[0].price, resp.json[0]["price"])
        self.assertListEqual(self.products[0].in_shops, resp.json[0]["in_shops"])
        self.assertEqual(self.products[0].listed, resp.json[0]["listed"])
        self.assertEqual(self.products[0].category.name, resp.json[0]["category"])

    def test_with_listed_products_user_expect_200_and_correct_json_len(self):
        resp = self.client.get(
            self.URL,
            headers=self._create_authorization_header(CustomerFactory))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json))

    def test_with_listed_products_not_auth_user_expect_200_and_correct_json_len(self):
        resp = self.client.get(
            self.URL)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json))

    def test_with_not_listed_and_listed_products_user_holder_expect_200_and_correct_json_len(self):
        [ProductFactory(holder_id=self.shop_owner.id, listed=False) for _ in range(4)]
        resp = self.client.get(
            self.URL,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(7, len(resp.json))

    def test_with_listed_products_from_two_shop_owners_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=True) for _ in range(4)]

        resp = self.client.get(
            self.URL,
            headers=self._create_authorization_header(CustomerFactory))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(7, len(resp.json))

    def test_with_not_listed_and_listed_products_from_two_shop_owners_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]

        resp = self.client.get(
            self.URL,
            headers=self._create_authorization_header(CustomerFactory))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json))

    def test_with_listed_and_not_products_admin_user_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]
        resp = self.client.get(
            self.URL,
            headers=self._create_authorization_header(AdminFactory))

        self.assertEqual(200, resp.status_code)
        self.assertEqual(7, len(resp.json))

    def test_with_listed_and_not_products_user_wants_all_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]
        [ProductFactory(holder_id=self.shop_owner.id, listed=False) for _ in range(5)]
        resp = self.client.get(
            self.URL,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(8, len(resp.json))

    def test_with_listed_and_not_products_user_wants_his_own_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]
        [ProductFactory(holder_id=self.shop_owner.id, listed=False) for _ in range(5)]
        url = self.URL + "?holder_id=" + str(self.shop_owner.id)
        resp = self.client.get(
            url,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(8, len(resp.json))

    def test_with_listed_and_not_products_user_wants_his_own_listed_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]
        [ProductFactory(holder_id=self.shop_owner.id, listed=False) for _ in range(5)]
        url = self.URL + "?listed=true"
        resp = self.client.get(
            url,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json))

    def test_with_listed_and_not_products_user_wants_his_own_listed_expect_200_and_correct_json_len(self):
        second_shop_owner = OwnerFactory()
        [ProductFactory(holder_id=second_shop_owner.id, listed=False) for _ in range(4)]
        products = [ProductFactory(holder_id=second_shop_owner.id, listed=True) for _ in range(5)]
        shop = ShopFactory(active=True, holder_id=self.shop_owner.id)
        [shop.products.append(product) for product in products]
        db.session.commit()

        url = self.URL + f"?shop_ids={shop.id}"
        resp = self.client.get(
            url,
            headers=self.authorization_headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(5, len(resp.json))
