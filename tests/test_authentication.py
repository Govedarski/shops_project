from werkzeug.security import generate_password_hash

from db import db
from managers.auth_manager import AuthManager
from models import CustomerModel, ShopOwnerModel
from schemas.validators.common_validators import ValidateIsAlphaNumeric
from tests import helpers as test_helpers
from tests.base_test_case import BaseTestCase
from utils import helpers


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
        self.assertIn("test is already taken", resp.json["message"]["username"])
        self.assertIn("test@test.com is already taken", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_owner_with_invalid_email_and_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "testtest.com", "password": "testP@ss1!", "role": "owner"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_invalid_email_and_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "testtest.com", "password": "testP@ss1!", "role": "customer"}
        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        test_helpers.assert_count_equal(0, CustomerModel)


class TestLogin(BaseTestCase):
    URL = "/login"
    VAlID_CREDENTIALS = {
        "username": "test",
        "email": "test@test.com",
        "password": "testP@ss1!",
    }

    def setUp(self):
        super().setUp()
        self._create_user_in_test_db("customer")
        self._create_user_in_test_db("owner")

    def _create_user_in_test_db(self, role):
        data = {**self.VAlID_CREDENTIALS, "role": role}
        data["password"] = generate_password_hash(data["password"])
        user_model = helpers.get_user_model(role)
        user = user_model(**data)
        db.session.add(user)
        db.session.commit()

    def test_login_with_customer_via_email_valid_credentials_expect_200_and_return_token(self):
        identifier = "email"
        role = "customer"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_customer_via_username_valid_credentials_expect_200_and_return_token(self):
        identifier = "username"
        role = "customer"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_owner_via_email_valid_credentials_expect_200_and_return_token(self):
        identifier = "email"
        role = "owner"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_owner_via_username_valid_credentials_expect_200_and_return_token(self):
        identifier = "username"
        role = "owner"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_customer_via_email_invalid_password_expect_400(self):
        identifier = "email"
        role = "customer"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_customer_via_username_invalid_password_expect_400(self):
        identifier = "username"
        role = "customer"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_owner_via_email_invalid_password_expect_400(self):
        identifier = "email"
        role = "owner"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_owner_via_username_invalid_password_expect_400(self):
        identifier = "username"
        role = "owner"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_customer_with_unexisting_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "customer"}

        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def test_login_with_owner_with_unexisting_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "owner"}

        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def _login_test(self, credentials_data, identifier, role, assertion_func):
        credentials = {
            "identifier": credentials_data[identifier],
            "password": credentials_data["password"],
            "role": role}

        resp = self.client.post(self.URL, headers=self._HEADERS_CONT_TYPE_JSON, json=credentials)
        assertion_func(resp, role)

    def _assert_successful_login(self, resp, role):
        self.assert200(resp)
        self.assertIn("token", resp.json)
        token = resp.json['token']

        self.assertEqual(role, AuthManager.decode_token(token)["role"])

    def _assert_login_fail(self, resp, *_):
        self.assert400(resp)
        self.assertEqual("Wrong credentials!", resp.json["message"])

    def _get_invalid_password_credentials(self):
        invalid_credentials = self.VAlID_CREDENTIALS.copy()
        invalid_credentials["password"] = "invalid_password"
        return invalid_credentials
