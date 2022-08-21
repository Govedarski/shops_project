from werkzeug.security import generate_password_hash

from db import db
from managers.auth_manager import AuthManager
from models import CustomerModel, ShopOwnerModel, AdminModel
from resources.helpers.access_endpoint_validators import ValidateRole
from schemas.validators.common_validators import ValidateIsAlphaNumeric
from tests import helpers as test_helpers
from tests.base_test_case import BaseTestCase
from tests.factories import SuperAdminFactory, AdminFactory
from tests.helpers import generate_token
from utils import helpers


class TestUserRegistration(BaseTestCase):
    URL = "/register"
    VALID_CUSTOMER_DATA = {"username": "test", "email": "test@test.com", "password": "testP@ss1!", "role": "customer"}
    VALID_OWNER_DATA = {"username": "test", "email": "test@test.com", "password": "testP@ss1!", "role": "owner"}

    def test_reg_customer_with_valid_data_expect_201_customer_added_to_db_and_return_token(self):
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assertEqual(201, resp.status_code)
        self.assertIn("token", resp.json)
        test_helpers.assert_count_equal(1, CustomerModel)
        test_helpers.assert_count_equal(0, ShopOwnerModel)

    def test_reg_owner_with_valid_data_expect_201_owner_added_to_db_and_return_token(self):
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_OWNER_DATA)

        self.assertEqual(201, resp.status_code)
        self.assertIn("token", resp.json)
        test_helpers.assert_count_equal(1, ShopOwnerModel)
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_valid_data_but_already_existing_username_and_email_expect_400_customer_not_added_to_db(
            self):
        self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)
        test_helpers.assert_count_equal(1, CustomerModel)

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assert400(resp)
        self.assertIn("test@test.com is already taken", resp.json["message"]["email"])
        self.assertIn("test is already taken", resp.json["message"]["username"])
        test_helpers.assert_count_equal(1, CustomerModel)

    def test_reg_customer_with_valid_data_but_shop_owner_with_same_email_and_username_existing_expect_400_and_not_added_to_db(
            self):
        self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_OWNER_DATA)
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.VALID_CUSTOMER_DATA)

        self.assert400(resp)
        self.assertIn("test is already taken", resp.json["message"]["username"])
        self.assertIn("test@test.com is already taken", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_owner_with_invalid_email_and_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "testtest.com", "password": "testP@ss1!", "role": "owner"}
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        test_helpers.assert_count_equal(0, CustomerModel)

    def test_reg_customer_with_invalid_email_and_username_expect_400_and_not_added_to_db(self):
        invalid_data = {"username": "test@", "email": "testtest.com", "password": "testP@ss1!", "role": "customer"}
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=invalid_data)
        self.assert400(resp)
        self.assertIn("Not a valid email address.", resp.json["message"]["email"])
        self.assertIn(ValidateIsAlphaNumeric.ERROR, resp.json["message"]["username"])
        test_helpers.assert_count_equal(0, CustomerModel)


class TestAdminRegistration(BaseTestCase):
    URL = "/admin/register"
    VAlID_CUSTOMER_CREDENTIALS = {
        "username": "test",
        "email": "test@test.com",
        "password": "testP@ss1!",
    }
    VAlID_OWNER_CREDENTIALS = {
        "username": "tester",
        "email": "tester@test.com",
        "password": "testP@ss1!",
    }
    VALID_CUSTOMER_DATA = {"role": "customer"}
    VALID_OWNER_DATA = {"role": "owner"}

    def setUp(self):
        super().setUp()
        self._super_admin = SuperAdminFactory()
        token = generate_token(self._super_admin)
        self._AUTHORIZATION_HEADER = {"Authorization": f"Bearer {token}"}
        self._HEADERS = self._AUTHORIZATION_HEADER | self._HEADER_CONT_TYPE_JSON
        self.customer = self._create_user_in_test_db("customer", self.VAlID_CUSTOMER_CREDENTIALS)
        self.owner = self._create_user_in_test_db("owner", self.VAlID_OWNER_CREDENTIALS)

    @staticmethod
    def _create_user_in_test_db(role, credentials):
        data = {**credentials, "role": role}
        data["password"] = generate_password_hash(data["password"])
        user_model = helpers.get_user_or_admin_model(role)
        user = user_model(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def test_create_admin_with_valid_user_expect_204(self):
        test_helpers.assert_count_equal(1, AdminModel)

        customer_url = self.URL + "/" + str(self.customer.id)
        resp = self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_CUSTOMER_DATA)
        self.assertEqual(204, resp.status_code)
        test_helpers.assert_count_equal(2, AdminModel)

        owner_url = self.URL + "/" + str(self.owner.id)
        resp = self.client.post(owner_url, headers=self._HEADERS, json=self.VALID_OWNER_DATA)
        self.assertEqual(204, resp.status_code)
        test_helpers.assert_count_equal(3, AdminModel)

    def test_create_admin_with_duplicate_user_expect_400(self):
        test_helpers.assert_count_equal(1, AdminModel)

        customer_url = self.URL + "/" + str(self.customer.id)
        self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_CUSTOMER_DATA)
        resp = self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_CUSTOMER_DATA)
        self.assertEqual(400, resp.status_code)
        self.assertIn("Unique constraint violation!", resp.json["message"])
        test_helpers.assert_count_equal(2, AdminModel)

        owner_url = self.URL + "/" + str(self.owner.id)
        self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_OWNER_DATA)
        resp = self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_OWNER_DATA)
        self.assertEqual(400, resp.status_code)
        self.assertIn("Unique constraint violation!", resp.json["message"])
        test_helpers.assert_count_equal(3, AdminModel)

    def test_create_admin_not_existing_user_expect_404_and_correct_message(self):
        customer_url = self.URL + "/" + str(self.customer.id + 1)
        self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_CUSTOMER_DATA)
        resp = self.client.post(customer_url, headers=self._HEADERS, json=self.VALID_CUSTOMER_DATA)
        self.assertEqual(404, resp.status_code)
        self.assertIn("Page not found!", resp.json["message"])

    def test_create_admin_from_not_super_admin_data_expect_403_and_correct_message(self):
        admin = AdminFactory()
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"} | self._HEADER_CONT_TYPE_JSON

        customer_url = self.URL + "/" + str(self.customer.id)
        resp = self.client.post(customer_url, headers=headers, json=self.VALID_CUSTOMER_DATA)
        self.assertEqual(403, resp.status_code)
        self.assertIn(ValidateRole.ERROR_MESSAGE, resp.json["message"])


class TestLogin(BaseTestCase):
    URL = "/login"
    VAlID_CREDENTIALS = {
        "username": "test",
        "email": "test@test.com",
        "password": "testP@ss1!",
    }
    VAlID_SUPER_ADMIN_CREDENTIALS = {
        "username": "test1",
        "email": "test1@test.com",
        "password": "test1P@ss1!",
    }

    def setUp(self):
        super().setUp()
        self._create_user_in_test_db("customer", self.VAlID_CREDENTIALS)
        self._create_user_in_test_db("owner", self.VAlID_CREDENTIALS)
        self._create_user_in_test_db("admin", self.VAlID_CREDENTIALS)
        self._create_user_in_test_db("super_admin", self.VAlID_SUPER_ADMIN_CREDENTIALS)

    @staticmethod
    def _create_user_in_test_db(role, credentials):
        data = {**credentials, "role": role}
        data["password"] = generate_password_hash(data["password"])
        user_model = helpers.get_user_or_admin_model(role)
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

    def test_login_with_admin_via_email_valid_credentials_expect_200_and_return_token(self):
        identifier = "email"
        role = "admin"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_admin_via_username_valid_credentials_expect_200_and_return_token(self):
        identifier = "username"
        role = "admin"
        self._login_test(self.VAlID_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_super_admin_via_email_valid_credentials_expect_200_and_return_token(self):
        identifier = "email"
        role = "super_admin"
        self._login_test(self.VAlID_SUPER_ADMIN_CREDENTIALS, identifier, role, self._assert_successful_login)

    def test_login_with_super_admin_via_username_valid_credentials_expect_200_and_return_token(self):
        identifier = "username"
        role = "super_admin"
        self._login_test(self.VAlID_SUPER_ADMIN_CREDENTIALS, identifier, role, self._assert_successful_login)

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

    def test_login_with_admin_via_email_invalid_password_expect_400(self):
        identifier = "email"
        role = "admin"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_admin_via_username_invalid_password_expect_400(self):
        identifier = "username"
        role = "admin"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_super_admin_via_email_invalid_password_expect_400(self):
        identifier = "email"
        role = "super_admin"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_super_admin_via_username_invalid_password_expect_400(self):
        identifier = "username"
        role = "super_admin"
        invalid_credentials = self._get_invalid_password_credentials()
        self._login_test(invalid_credentials, identifier, role, self._assert_login_fail)

    def test_login_with_customer_with_not_existing_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "customer"}

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def test_login_with_owner_with_not_existing_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "owner"}

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def test_login_with_admin_with_not_existing_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "admin"}

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def test_login_with_super_admin_with_not_existing_identifier_expect_400(self):
        credentials = {
            "identifier": "not_existing",
            "password": "some_password",
            "role": "super_admin"}

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=credentials)

        self._assert_login_fail(resp)

    def _login_test(self, credentials_data, identifier, role, assertion_func):
        credentials = {
            "identifier": credentials_data[identifier],
            "password": credentials_data["password"],
            "role": role}

        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=credentials)
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
