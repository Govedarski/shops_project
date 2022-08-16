from models import CustomerModel, ShopOwnerModel
from schemas.validators.common_validators import ValidateIsAlphaNumeric
from tests import helpers as test_helpers
from tests.base_test_case import BaseTestCase


class TestRegistration(BaseTestCase):
    URL = "/register"
    VALID_CUSTOMER_DATA = {"username": "test", "email": "test@test.com", "password": "testP@ss1!", "role": "customer"}
    VALID_OWNER_DATA = {"username": "test", "email": "test@test.com", "password": "testP@ss1!", "role": "owner"}

    def test_reg_customer_with_valid_data_expect_201_customer_added_to_db_and_return_token(self):
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assertEqual(resp.status_code, 201)
        self.assertIn("token", resp.json)
        test_helpers.assert_count_equal(1, CustomerModel)
        test_helpers.assert_count_equal(0, ShopOwnerModel)

    def test_reg_owner_with_valid_data_expect_201_owner_added_to_db_and_return_token(self):
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_OWNER_DATA)

        self.assertEqual(resp.status_code, 201)
        self.assertIn("token", resp.json)
        test_helpers.assert_count_equal(1, ShopOwnerModel)
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_valid_data_but_already_existing_username_and_email_expect_400_customer_not_added_to_db(
            self):
        self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)
        test_helpers.assert_count_equal(1, CustomerModel)

        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assert400(resp)
        self.assertIn("test@test.com is already taken", resp.json["message"]["email"])
        self.assertIn("test is already taken", resp.json["message"]["username"])
        test_helpers.assert_count_equal(1, CustomerModel)

    def test_reg_customer_with_valid_data_but_shop_owner_with_same_email_and_username_existing_expect_400_and_not_added_to_db(
            self):
        self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_OWNER_DATA)
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assert400(resp)
        self.assertIn("test@test.com is already taken", resp.json["message"]["email"])
        self.assertIn("test is already taken", resp.json["message"]["username"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_owner_with_invalid_email_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test", "email": "testtest.com", "password": "testP@ss1!", "role": "owner"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_invalid_email_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test", "email": "testtest.com", "password": "testP@ss1!", "role": "customer"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_owner_with_invalid_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "test@test.com", "password": "testP@ss1!", "role": "owner"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_invalid_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "test@test.com", "password": "testP@ss1!", "role": "customer"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        test_helpers.assert_count_equal(0, CustomerModel)
