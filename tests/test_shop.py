from unittest.mock import patch

from db import db
from models import ShopModel
from services.s3 import s3
from tests import helpers
from tests.base_test_case import BaseTestCase
from tests.constants import ENCODED_PICTURE
from tests.factories import OwnerFactory, AdminFactory, CustomerFactory
from tests.helpers import generate_token


class TestApp(BaseTestCase):
    URL = "/shop"
    VALID_DATA = {
        "name": "Testov shop",
        "bulstat": "123465789",
        "city": "Testov grad",
        "address": "My test address",
        "verifying_documents_photo": ENCODED_PICTURE,
        "verifying_documents_extension": "pdf",
    }

    VALID_BRAND_PHOTO_DATA = {
        "brand_logo_photo": ENCODED_PICTURE,
        "brand_logo_extension": "png",
    }

    _created_shops = 0

    def setUp(self):
        super().setUp()
        self._shop_owner = OwnerFactory()
        token = generate_token(self._shop_owner)
        self._AUTHORIZATION_HEADER = {"Authorization": f"Bearer {token}"}
        self._HEADERS = self._HEADER_CONT_TYPE_JSON | self._AUTHORIZATION_HEADER

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def _get_create_data(self, active, verified=None):
        if verified is None:
            verified = active
        self._created_shops += 1
        return {
            "name": f"Testov shop {str(self._created_shops)}",
            "bulstat": "123465789",
            "city": "Testov grad",
            "address": "My test address",
            "verifying_documents_image_url": "tes_url",
            "active": active,
            "verified": verified,
        }

    @staticmethod
    def _create_in_db(model, data, holder_id):
        instance = model(holder_id=holder_id, **data)
        db.session.add(instance)
        db.session.commit()
        return instance

    def _test_schema_out(self, resp, extended=True):
        assertion_func = self.assertIn if extended else self.assertNotIn
        assertion_func("bulstat", resp)
        assertion_func("address", resp)
        assertion_func("phone_number", resp)
        assertion_func("verifying_documents_image_url", resp)
        assertion_func("verified", resp)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_create_shop_with_valid_data_expect_201_correct_json_and_record_in_db(self, mocked_s3):
        data = self.VALID_DATA | self.VALID_BRAND_PHOTO_DATA

        resp = self.client.post(self.URL, headers=self._HEADERS, json=data)

        self.assertEqual(201, resp.status_code)
        helpers.assert_count_equal(1, ShopModel)
        self.assertEqual(self.VALID_DATA["name"], resp.json["name"])
        self.assertEqual(self.VALID_DATA["bulstat"], resp.json["bulstat"])
        self.assertEqual(self.VALID_DATA["city"], resp.json["city"])
        self.assertEqual(self.VALID_DATA["address"], resp.json["address"])
        self.assertEqual(self.VALID_DATA["address"], resp.json["address"])
        self.assertEqual(self._shop_owner.id, resp.json["holder_id"])
        self.assertEqual(mocked_s3.return_value, resp.json["verifying_documents_image_url"])
        self.assertEqual(mocked_s3.return_value, resp.json["brand_logo_image_url"])
        self.assertFalse(resp.json["verified"])
        self.assertFalse(resp.json["active"])

    def test_create_shop_with_invalid_data_expect_400_correct_json_and_no_record_in_db(self):
        invalid_data = {
            "name": "T",
            "bulstat": "123465b9",
            "city": "1",
            "verifying_documents_extension": "xml",
        }

        resp = self.client.post(self.URL, headers=self._HEADERS, json=invalid_data)

        self.assertEqual(400, resp.status_code)
        helpers.assert_count_equal(0, ShopModel)
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["name"])
        self.assertIn("Length must be 9.", resp.json["message"]["bulstat"])
        self.assertIn("Must contain only numbers!", resp.json["message"]["bulstat"])
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["city"])
        self.assertIn("Must contain only letters and spaces!", resp.json["message"]["city"])
        self.assertIn("Missing data for required field.", resp.json["message"]["address"])
        self.assertIn(
            "Valid extension for documents are jpg, jpeg, png, pdf!",
            resp.json["message"]["verifying_documents_extension"])

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_create_2_shops_with_same_name_expect_400_correct_json_and_no_record_in_db(self, mocked_s3):
        self.client.post(self.URL, headers=self._HEADERS, json=self.VALID_DATA)
        resp = self.client.post(self.URL, headers=self._HEADERS, json=self.VALID_DATA)

        self.assertEqual(400, resp.status_code)
        helpers.assert_count_equal(1, ShopModel)
        self.assertIn("Testov shop is already taken", resp.json["message"]["name"])

    def test_get_shops_and_schema_out_without_query_params_expect_200_and_list_of_all(self):
        [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(True), second_shop_owner.id) for _ in range(6)]

        resp = self.client.get(self.URL, headers=self._AUTHORIZATION_HEADER)
        extended_schema_out_items = [item for item in resp.json if item.get("holder_id") == self._shop_owner.id]
        short_schema_out_items = [item for item in resp.json if item.get("holder_id") != self._shop_owner.id]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(10, len(resp.json))
        self._test_schema_out(extended_schema_out_items[0])
        self._test_schema_out(short_schema_out_items[0], extended=False)

    def test_get_shops_with_not_auth_user_expect_200_and_short_schema_out(self):
        [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(True), second_shop_owner.id) for _ in range(6)]

        resp = self.client.get(self.URL)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(10, len(resp.json))
        self._test_schema_out(resp.json[0], extended=False)

    def test_get_shops_with_admin_user_expect_200_and_extend_schema_out(self):
        [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(True), second_shop_owner.id) for _ in range(6)]

        resp = self.client.get(self.URL, headers=self._create_authorization_header(AdminFactory))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(10, len(resp.json))
        self._test_schema_out(resp.json[0])

    def test_get_shops_with_query_params_expect_200_and_filter_list_of_shop(self):
        item = [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)][0]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(True), second_shop_owner.id) for _ in range(6)]

        url = self.URL + f"?holder_id={second_shop_owner.id}"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(6, len(resp.json))

        url = self.URL + f"?holder_id={self._shop_owner.id}&name={item.name}"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, len(resp.json))

        url = self.URL + f"?holder_id=5&name={item.name}"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(resp.json))

        url = self.URL + f"?holder=pesho&name={item.name}"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(0, len(resp.json))

    def test_get_single_shop_holder_user_expect_200_and_correct_json(self):
        [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)]
        item = self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id)
        [self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id) for _ in range(4)]
        url = self.URL + "/" + str(item.id)

        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self._test_schema_out(resp.json)
        self.assertEqual(item.name, resp.json["name"])

    def test_get_single_shop_admin_user_expect_200_and_correct_json(self):
        item = self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id)
        url = self.URL + "/" + str(item.id)

        resp = self.client.get(url, headers=self._create_authorization_header(AdminFactory))
        self.assertEqual(200, resp.status_code)
        self._test_schema_out(resp.json)

    def test_get_single_shop_not_holder_user_expect_200_and_correct_json(self):
        item = self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id)
        url = self.URL + "/" + str(item.id)

        resp = self.client.get(url, headers=self._create_authorization_header(CustomerFactory))
        self.assertEqual(200, resp.status_code)
        self._test_schema_out(resp.json, extended=False)

        resp = self.client.get(url, headers=self._create_authorization_header(OwnerFactory))
        self.assertEqual(200, resp.status_code)
        self._test_schema_out(resp.json, extended=False)

    def test_get_single_shop_no_auth_user_expect_200_and_correct_json(self):
        item = self._create_in_db(ShopModel, self._get_create_data(True), self._shop_owner.id)
        url = self.URL + "/" + str(item.id)

        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self._test_schema_out(resp.json, extended=False)

    def test_get_single_shop_with_no_auth_user_and_inactive_shop_expect_403(self):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id)
        url = self.URL + "/" + str(shop.id)

        resp = self.client.get(url)
        self.assertEqual(403, resp.status_code)

    def test_get_with_holder_and_inactive_shop_expect_200_and_list_of_all_shops(self):
        [self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id) for _ in range(4)]
        resp = self.client.get(self.URL, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(4, len(resp.json))

    def test_get_with_admin_and_inactive_shop_expect_200_and_list_of_all_shops(self):
        [self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id) for _ in range(4)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id) for _ in range(3)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(active=False), second_shop_owner.id) for _ in range(5)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), second_shop_owner.id) for _ in range(6)]
        resp = self.client.get(self.URL, headers=self._create_authorization_header(AdminFactory))
        self.assertEqual(200, resp.status_code)
        self.assertEqual(18, len(resp.json))

    def test_get_with_no_auth_user_and_inactive_shop_expect_200_and_empty_list(self):
        [self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id) for _ in range(4)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id) for _ in range(3)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(active=False), second_shop_owner.id) for _ in range(5)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), second_shop_owner.id) for _ in range(6)]
        resp = self.client.get(self.URL)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(9, len(resp.json))

    def test_get_with_no_holder_of_part_of_shops_and_inactive_shops_expect_200_and_filter_list_of_shops(self):
        [self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id) for _ in range(4)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id) for _ in range(3)]
        second_shop_owner = OwnerFactory()
        [self._create_in_db(ShopModel, self._get_create_data(active=False), second_shop_owner.id) for _ in range(5)]
        [self._create_in_db(ShopModel, self._get_create_data(active=True), second_shop_owner.id) for _ in range(6)]

        resp = self.client.get(self.URL, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(13, len(resp.json))

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_edit_not_verified_with_name_and_bulstat_expect_status_200_db_updated_correct_json(self, mocked_s3):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=False), self._shop_owner.id)

        url = self.URL + "/" + str(shop.id)
        data = {"name": "Edited Shop",
                "bulstat": "987654321",
                "city": "Edited city",
                } | self.VALID_BRAND_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(data["name"], resp.json["name"])
        self.assertEqual(data["bulstat"], resp.json["bulstat"])
        self.assertEqual(data["city"], resp.json["city"])
        self.assertEqual(mocked_s3.return_value, resp.json["brand_logo_image_url"])
        self.assertEqual(data["name"], shop.name)
        self.assertEqual(data["bulstat"], shop.bulstat)
        self.assertEqual(data["city"], shop.city)
        self.assertEqual(mocked_s3.return_value, shop.brand_logo_image_url)

    def test_edit_verified_with_name_and_bulstat_expect_status_400_and_correct_json(self):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id)

        url = self.URL + "/" + str(shop.id)
        data = {"name": "Edited Shop",
                "bulstat": "987654321",
                "city": "Edited city",
                } | self.VALID_BRAND_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(400, resp.status_code)
        self.assertIn("name", resp.json["message"])
        self.assertIn("bulstat", resp.json["message"])

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_edit_verified_without_name_and_bulstat_expect_status_200_db_updated_correct_json(self, mocked_s3):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id)

        url = self.URL + "/" + str(shop.id)
        data = {"city": "Edited city",
                } | self.VALID_BRAND_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(data["city"], resp.json["city"])
        self.assertEqual(mocked_s3.return_value, resp.json["brand_logo_image_url"])
        self.assertEqual(data["city"], shop.city)
        self.assertEqual(mocked_s3.return_value, shop.brand_logo_image_url)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_change_profile_picture_with_valid_data_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id)

        url = self.URL + "/" + str(shop.id)
        data = self.VALID_BRAND_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(mocked_s3.return_value, resp.json["brand_logo_image_url"])
        self.assertEqual(mocked_s3.return_value, shop.brand_logo_image_url)

    @patch.object(s3, "delete_photo", return_value=None)
    def test_delete_existing_brand_logo_picture_expect_status_200_db_updated_correct_json(self, _):
        data = self._get_create_data(active=True) | {"brand_logo_image_url": "some.url"}

        shop = self._create_in_db(ShopModel, data, self._shop_owner.id)
        url = self.URL + "/" + str(shop.id) + "/brand_logo"

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(None, resp.json["brand_logo_image_url"])

    def test_delete_not_existing_profile_picture_expect_status_404_and_correct_message(self):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id)
        url = self.URL + "/" + str(shop.id) + "/brand_logo"
        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(404, resp.status_code)

    def test_verify_information_admin_user_expect_200_and_change_in_db(self):
        shop = self._create_in_db(ShopModel, self._get_create_data(active=True), self._shop_owner.id)

        url = self.URL + "/" + str(shop.id) + "/verify"

        resp = self.client.put(url, headers=self._create_authorization_header(AdminFactory))

        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.json["verified"])
        self.assertTrue(resp.json["active"])
        self.assertTrue(shop.verified)
        self.assertTrue(shop.active)
