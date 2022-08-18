from unittest.mock import patch

from db import db
from models import CustomerDetailsModel
from services.s3 import s3
from tests import helpers
from tests.base_test_case import BaseTestCase
from tests.constants import ENCODED_PICTURE
from tests.factories import CustomerFactory
from tests.helpers import generate_token


class TestCustomerDetails(BaseTestCase):
    BASE_URL = "/customer/details"
    CREATE_URL = BASE_URL + "/create"
    VALID_REQUIRED_DATA = {
        "first_name": "Testcho",
        "last_name": "Testchov",
    }
    VALID_PHOTO_DATA = {
        "photo": ENCODED_PICTURE,
        "extension": "jpg",
    }

    def setUp(self):
        super().setUp()
        self._customer = CustomerFactory()
        token = generate_token(self._customer)
        self._AUTHORIZATION_HEADER = {"Authorization": f"Bearer {token}"}
        self._HEADERS = self._AUTHORIZATION_HEADER | self._HEADER_CONT_TYPE_JSON

    def test_create_cd_with_valid_data_and_no_photo_expect_status_201_and_details_created_with_correct_data(self):
        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(self.VALID_REQUIRED_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.VALID_REQUIRED_DATA["last_name"], resp.json["last_name"])
        self.assertEqual(None, resp.json["profile_picture_url"])
        helpers.assert_count_equal(1, CustomerDetailsModel)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_create_cd_with_valid_data_and_photo_expect_status_201_and_details_created_with_correct_json(self,
                                                                                                         mocked_s3):
        data = self.VALID_REQUIRED_DATA | self.VALID_PHOTO_DATA

        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=data)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(self.VALID_REQUIRED_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.VALID_REQUIRED_DATA["last_name"], resp.json["last_name"])
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_url"])

    def test_create_cd_with_valid_data_and_creator_who_already_has_cd_expect_status_403_and_correct_error_message(self):
        self.client.post(self.CREATE_URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)
        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)

        self.assertEqual(403, resp.status_code)
        self.assertEqual(f"User with id: {self._customer.id} has already created details!", resp.json["message"])

    def test_create_cd_with_partly_missing_photo_data_expect_status_400_and_correct_error_messages(self):
        data_no_extension = self.VALID_REQUIRED_DATA | {
            "photo": ENCODED_PICTURE,
        }
        data_no_photo = self.VALID_REQUIRED_DATA | {
            "extension": "png",
        }
        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=data_no_extension)

        self.assertEqual(400, resp.status_code)
        self.assertEqual("There is not extension provided!", resp.json["message"])

        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=data_no_photo)

        self.assertEqual(400, resp.status_code)
        self.assertEqual("There is not photo provided!", resp.json["message"])

    def test_create_cd_with_invalid_data_expect_status_400_and_correct_error_messages(self):
        invalid_data = {
            "first_name": "1",
            "last_name": "2",
            "phone_number": "123",
            "age": 15,
            "photo": ENCODED_PICTURE,
            "extension": "txt"
        }
        resp = self.client.post(self.CREATE_URL, headers=self._HEADERS, json=invalid_data)
        self.assertEqual(400, resp.status_code)
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["first_name"])
        self.assertIn("Must contain only letters!", resp.json["message"]["first_name"])
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["last_name"])
        self.assertIn("Must contain only letters!", resp.json["message"]["last_name"])
        self.assertIn("Must be greater than or equal to 16 and less than or equal to 100.", resp.json["message"]["age"])
        self.assertIn("Length must be 9.", resp.json["message"]["phone_number"])
        self.assertIn("Valid photo extensions are jpg and jpeg and png!", resp.json["message"]["extension"])

    def test_get_cd_with_existing_cd_expect_status_200_and_correct_json(self):
        customer_details = self._create_customer_details_in_test_db(self.VALID_REQUIRED_DATA)
        url = self.BASE_URL + "/" + str(customer_details.id)
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(self.VALID_REQUIRED_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.VALID_REQUIRED_DATA["last_name"], resp.json["last_name"])

    def test_get_cd_with_not_existing_cd_expect_status_404_and_correct_message(self):
        url = self.BASE_URL + "/" + "1"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(404, resp.status_code)
        self.assertEqual(f"Details with id: 1 are not found!", resp.json["message"])

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_edit_with_valid_data_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        customer_details = self._create_customer_details_in_test_db(self.VALID_REQUIRED_DATA)
        url = self.BASE_URL + "/" + str(customer_details.id)
        data = {"first_name": "TestchoEdit",
                "last_name": "TestchovEdit"} | self.VALID_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(data["first_name"], resp.json["first_name"])
        self.assertEqual(data["last_name"], resp.json["last_name"])
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_url"])
        self.assertEqual(data["first_name"], customer_details.first_name)
        self.assertEqual(data["last_name"], customer_details.last_name)
        self.assertEqual(mocked_s3.return_value, customer_details.profile_picture_url)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_change_profile_picture_with_valid_data_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        customer_details = self._create_customer_details_in_test_db(self.VALID_REQUIRED_DATA)
        url = self.BASE_URL + "/" + str(customer_details.id) + "/profile_picture"
        data = self.VALID_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_url"])
        self.assertEqual(mocked_s3.return_value, customer_details.profile_picture_url)

    @patch.object(s3, "delete_photo", return_value=None)
    def test_delete_existing_profile_picture_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        data = self.VALID_REQUIRED_DATA | {"profile_picture_url": "some.url"}
        customer_details = self._create_customer_details_in_test_db(data)
        url = self.BASE_URL + "/" + str(customer_details.id) + "/profile_picture"

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(None, resp.json["profile_picture_url"])

    def test_delete_not_existing_profile_picture_expect_status_404_and_correct_message(self):
        customer_details = self._create_customer_details_in_test_db(self.VALID_REQUIRED_DATA)
        url = self.BASE_URL + "/" + str(customer_details.id) + "/profile_picture"

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(404, resp.status_code)

    def _create_customer_details_in_test_db(self, data):
        customer_details = CustomerDetailsModel(customer_id=self._customer.id, **data)
        db.session.add(customer_details)
        db.session.commit()
        return customer_details
