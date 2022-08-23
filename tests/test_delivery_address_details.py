from db import db
from managers.auth_manager import AuthManager
from models import DeliveryAddressDetailsModel, CustomerDetailsModel
from resources.helpers.access_endpoint_validators import ValidateRole
from tests import helpers
from tests.base_test_case import BaseTestCase
from tests.factories import CustomerFactory, AdminFactory, OwnerFactory
from tests.helpers import generate_token, assert_count_equal


class TestShopOwnerDetails(BaseTestCase):
    URL = "/delivery_address_details"
    DATA_NO_AUTH = {
        "first_name": "Testcho",
        "last_name": "Testchov",
    }
    DATA_AUTH = {
        "phone_number": "883123456",
        "city": "Testov grad",
        "address": "My test address",
        "extra_informations": "Bring me cofffee. It's urgent!"
    }

    DATA = DATA_NO_AUTH | DATA_AUTH

    def setUp(self):
        super().setUp()
        self._customer = CustomerFactory()
        token = generate_token(self._customer)
        self._AUTHORIZATION_HEADER = {"Authorization": f"Bearer {token}"}
        self._HEADERS = self._AUTHORIZATION_HEADER | self._HEADER_CONT_TYPE_JSON

    @staticmethod
    def _create_in_db(model, data, holder_id):
        instance = model(holder_id=holder_id, **data)
        db.session.add(instance)
        db.session.commit()
        return instance

    @staticmethod
    def _create_authorization_header(factory):
        user = factory()
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def test_create_DAD_with_no_auth_user_expect_201_correct_json_and_record_in_db(self):
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.DATA)

        self.assertEqual(201, resp.status_code)
        helpers.assert_count_equal(1, DeliveryAddressDetailsModel)
        self.assertEqual(self.DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.DATA["last_name"], resp.json["last_name"])
        self.assertEqual(self.DATA["phone_number"], resp.json["phone_number"])
        self.assertEqual(self.DATA["city"], resp.json["city"])
        self.assertEqual(self.DATA["address"], resp.json["address"])
        self.assertEqual(self.DATA["extra_informations"], resp.json["extra_informations"])

    def test_create_DAD_with_no_auth_user_and_not_enough_data_expect_400(self):
        resp = self.client.post(self.URL, headers=self._HEADER_CONT_TYPE_JSON, json=self.DATA_AUTH)

        self.assertEqual(400, resp.status_code)
        helpers.assert_count_equal(0, DeliveryAddressDetailsModel)
        self.assertIn("first_name", resp.json["message"])
        self.assertIn("last_name", resp.json["message"])

    def test_create_DAD_with_customer_with_no_details_expect_201_correct_json_and_record_in_db(self):
        resp = self.client.post(self.URL, headers=self._HEADERS, json=self.DATA)

        self.assertEqual(201, resp.status_code)
        helpers.assert_count_equal(1, DeliveryAddressDetailsModel)
        helpers.assert_count_equal(1, CustomerDetailsModel)
        self.assertEqual(self.DATA["phone_number"], resp.json["phone_number"])
        self.assertEqual(self.DATA["city"], resp.json["city"])
        self.assertEqual(self.DATA["address"], resp.json["address"])
        self.assertEqual(self.DATA["extra_informations"], resp.json["extra_informations"])

    def test_create_DAD_with_shop_owner_expect_403(self):
        data = self.DATA_AUTH
        self._create_in_db(CustomerDetailsModel, self.DATA_NO_AUTH, self._customer.id)

        resp = self.client.post(self.URL, headers=self._HEADERS, json=data)

        self.assertEqual(201, resp.status_code)
        helpers.assert_count_equal(1, DeliveryAddressDetailsModel)
        self.assertEqual(self._customer.details.first_name, resp.json["first_name"])
        self.assertEqual(self._customer.details.last_name, resp.json["last_name"])
        self.assertEqual(data["phone_number"], resp.json["phone_number"])
        self.assertEqual(data["city"], resp.json["city"])
        self.assertEqual(data["address"], resp.json["address"])
        self.assertEqual(data["extra_informations"], resp.json["extra_informations"])

    def test_get_DAD_with_customer_holder_expect_200_and_correct_json(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)

        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(details.first_name, resp.json["first_name"])
        self.assertEqual(details.last_name, resp.json["last_name"])
        self.assertEqual(details.phone_number, resp.json["phone_number"])
        self.assertEqual(details.city, resp.json["city"])
        self.assertEqual(details.address, resp.json["address"])
        self.assertEqual(details.extra_informations, resp.json["extra_informations"])

    def test_get_DAD_with_admin_expect_200_and_correct_json(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        headers = self._create_authorization_header(AdminFactory)

        resp = self.client.get(url, headers=headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(details.first_name, resp.json["first_name"])
        self.assertEqual(details.last_name, resp.json["last_name"])
        self.assertEqual(details.phone_number, resp.json["phone_number"])
        self.assertEqual(details.city, resp.json["city"])
        self.assertEqual(details.address, resp.json["address"])
        self.assertEqual(details.extra_informations, resp.json["extra_informations"])

    def test_get_DAD_with_customer_not_holder_expect_403(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        headers = self._create_authorization_header(CustomerFactory)

        resp = self.client.get(url, headers=headers)

        self.assertEqual(403, resp.status_code)
        self.assertEqual(ValidateRole.ERROR_MESSAGE, resp.json["message"])

    def test_get_DAD_with_shop_owner_expect_403(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        headers = self._create_authorization_header(OwnerFactory)

        resp = self.client.get(url, headers=headers)

        self.assertEqual(403, resp.status_code)
        self.assertEqual(ValidateRole.ERROR_MESSAGE, resp.json["message"])

    def test_get_no_auth_user_expect_401(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)

        resp = self.client.get(url)

        self.assertEqual(401, resp.status_code)
        self.assertEqual(AuthManager.MISSING_TOKEN_MESSAGE, resp.json["message"])

    def test_edit_customer_holder_expect_200_and_correct_json(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        edit_data = {"city": "Edited City"}

        resp = self.client.put(url, headers=self._HEADERS, json=edit_data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(edit_data["city"], resp.json["city"])
        self.assertEqual(edit_data["city"], details.city)

    def test_edit_admin_expect_200_and_correct_json(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        edit_data = {"city": "Edited City"}
        headers = self._create_authorization_header(AdminFactory)

        resp = self.client.put(url, headers=headers, json=edit_data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(edit_data["city"], resp.json["city"])
        self.assertEqual(edit_data["city"], details.city)

    def test_get_list_customer_holder_expect_200_and_correct_json(self):
        [self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id) for _ in range(4)]
        second_customer = CustomerFactory()
        [self._create_in_db(DeliveryAddressDetailsModel, self.DATA, second_customer.id) for _ in range(6)]

        resp = self.client.get(self.URL, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(4, len(resp.json))
        self.assertTrue(all([details["holder_id"] == self._customer.id for details in resp.json]))

    def test_get_list_customer_holder_expect_200_and_empty_list(self):
        second_customer = CustomerFactory()
        [self._create_in_db(DeliveryAddressDetailsModel, self.DATA, second_customer.id) for _ in range(6)]

        resp = self.client.get(self.URL, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertListEqual([], resp.json)

    def test_get_list_admin_expect_200_and_correct_json(self):
        [self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id) for _ in range(4)]
        second_customer = CustomerFactory()
        [self._create_in_db(DeliveryAddressDetailsModel, self.DATA, second_customer.id) for _ in range(6)]
        headers = self._create_authorization_header(AdminFactory)

        resp = self.client.get(self.URL, headers=headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(10, len(resp.json))

    def test_delete_with_holder_no_order_linked_expect_204_and_record_in_db(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        assert_count_equal(1, DeliveryAddressDetailsModel)
        url = self.URL + "/" + str(details.id)

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(204, resp.status_code)
        assert_count_equal(0, DeliveryAddressDetailsModel)

    def test_delete_with_admin_no_order_linked_expect_204_and_record_in_db(self):
        details = self._create_in_db(DeliveryAddressDetailsModel, self.DATA, self._customer.id)
        url = self.URL + "/" + str(details.id)
        headers = self._create_authorization_header(AdminFactory)

        resp = self.client.delete(url, headers=headers)

        self.assertEqual(204, resp.status_code)
        assert_count_equal(0, DeliveryAddressDetailsModel)

    # TODO add test for delete when is linked to order forbidden expected
