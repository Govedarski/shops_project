from unittest.mock import patch

from db import db
from models import ShopOwnerModel, ShopOwnerDetailsModel
from resources.details_resources.shop_owner_details_resources import ShopOwnerDetailsResource
from resources.helpers.access_endpoint_validators import ValidateUniqueness
from services.s3 import s3
from tests import helpers
from tests.base_test_case import BaseTestCase
from tests.constants import ENCODED_PICTURE
from tests.factories import OwnerFactory, AdminFactory
from tests.helpers import generate_token


class TestShopOwnerDetails(BaseTestCase):
    URL = "/shop_owner/details"
    VALID_REQUIRED_DATA = {
        "first_name": "Testcho",
        "last_name": "Testchov",
        "iban": "DE89 3704 0044 0532 0130 00",
        "confirm_identity_documents_photo": ENCODED_PICTURE,
        "confirm_identity_documents_extension": "jpg",
    }
    VALID_PHOTO_DATA = {
        "profile_picture_photo": ENCODED_PICTURE,
        "profile_picture_extension": "jpg",
    }

    SHOP_OWNER_DETAILS_DATA = {
        "first_name": "Testcho",
        "last_name": "Testchov",
        "iban": "DE89370400440532013000",
        "confirm_identity_documents_image_url": "some_url",
    }

    def setUp(self):
        super().setUp()
        self._owner = OwnerFactory()
        token = generate_token(self._owner)
        self._AUTHORIZATION_HEADER = {"Authorization": f"Bearer {token}"}
        self._HEADERS = self._AUTHORIZATION_HEADER | self._HEADER_CONT_TYPE_JSON

    def _create_owner_details_in_test_db(self, data=None):
        data = data if data else self.SHOP_OWNER_DETAILS_DATA
        details = ShopOwnerDetailsModel(holder_id=self._owner.id, **data)
        db.session.add(details)
        db.session.commit()
        return details

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_create_so_with_valid_data_and_no_photo_expect_status_201_and_details_created_with_correct_data(self,
                                                                                                            mocked_s3):
        resp = self.client.post(self.URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(self.VALID_REQUIRED_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.VALID_REQUIRED_DATA["last_name"], resp.json["last_name"])
        self.assertEqual(self.VALID_REQUIRED_DATA["iban"].replace(" ", ""), resp.json["iban"])
        self.assertEqual(mocked_s3.return_value, resp.json["confirm_identity_documents_image_url"])
        self.assertEqual(None, resp.json["profile_picture_image_url"])
        helpers.assert_count_equal(1, ShopOwnerModel)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_create_so_with_valid_data_and_photo_expect_status_201_and_details_created_with_correct_json(self,
                                                                                                         mocked_s3):
        data = self.VALID_REQUIRED_DATA | self.VALID_PHOTO_DATA

        resp = self.client.post(self.URL, headers=self._HEADERS, json=data)

        self.assertEqual(201, resp.status_code)
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_image_url"])

    def test_create_so_with_valid_data_and_creator_who_already_has_cd_expect_status_403_and_correct_error_message(self):
        self.client.post(self.URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)
        resp = self.client.post(self.URL, headers=self._HEADERS, json=self.VALID_REQUIRED_DATA)

        self.assertEqual(403, resp.status_code)
        self.assertEqual(ValidateUniqueness.ERROR_MESSAGE, resp.json["message"])

    def test_create_so_with_invalid_data_expect_status_400_and_correct_error_messages(self):
        invalid_data = {
            "first_name": "1",
            "last_name": "2",
            "phone_number": "123",
            "age": 15,
            "confirm_identity_documents_photo": ENCODED_PICTURE,
            "confirm_identity_documents_extension": "jprg",
            "profile_picture_photo": ENCODED_PICTURE,
            "profile_picture_extension": "txt"
        }
        resp = self.client.post(self.URL, headers=self._HEADERS, json=invalid_data)
        self.assertEqual(400, resp.status_code)
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["first_name"])
        self.assertIn("Must contain only letters!", resp.json["message"]["first_name"])
        self.assertIn("Length must be between 2 and 64.", resp.json["message"]["last_name"])
        self.assertIn("Must contain only letters!", resp.json["message"]["last_name"])
        self.assertIn("Must be greater than or equal to 18 and less than or equal to 100.", resp.json["message"]["age"])
        self.assertIn("Length must be 9.", resp.json["message"]["phone_number"])
        self.assertIn("Valid extension for photos are jpg, jpeg, png!",
                      resp.json["message"]["profile_picture_extension"])
        self.assertIn("Valid extension for documents are jpg, jpeg, png, pdf!",
                      resp.json["message"]["confirm_identity_documents_extension"])

    def test_get_so_with_owner_expect_status_200_and_correct_json(self):
        details = self._create_owner_details_in_test_db()
        url = self.URL + "/" + str(details.id)
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["last_name"], resp.json["last_name"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["iban"], resp.json["iban"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["confirm_identity_documents_image_url"],
                         resp.json["confirm_identity_documents_image_url"])
        # self.assertNotIn("iban", resp.json)
        # self.assertNotIn("confirm_identity_documents_image_url", resp.json)

    def test_get_so_with_not_owner_expect_status_200_and_correct_json(self):
        new_owner = OwnerFactory()

        data = self.SHOP_OWNER_DETAILS_DATA | {"holder_id": new_owner.id}

        details = ShopOwnerDetailsModel(**data)
        db.session.add(details)
        db.session.commit()

        url = self.URL + "/" + str(details.id)
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(data["first_name"], resp.json["first_name"])
        self.assertEqual(data["last_name"], resp.json["last_name"])
        self.assertNotIn("iban", resp.json)
        self.assertNotIn("confirm_identity_documents_image_url", resp.json)

    def test_get_so_with_admin_expect_status_200_and_correct_json(self):
        admin = AdminFactory()
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"} | self._HEADER_CONT_TYPE_JSON

        details = self._create_owner_details_in_test_db()
        url = self.URL + "/" + str(details.id)

        resp = self.client.get(url, headers=headers)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["first_name"], resp.json["first_name"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["last_name"], resp.json["last_name"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["iban"], resp.json["iban"])
        self.assertEqual(self.SHOP_OWNER_DETAILS_DATA["confirm_identity_documents_image_url"],
                         resp.json["confirm_identity_documents_image_url"])

    def test_get_cd_with_not_existing_cd_expect_status_404_and_correct_message(self):
        url = self.URL + "/" + "1"
        resp = self.client.get(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(404, resp.status_code)
        self.assertEqual(ShopOwnerDetailsResource.NOT_FOUND_MESSAGE, resp.json["message"])

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_edit_with_valid_data_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        details = self._create_owner_details_in_test_db()

        url = self.URL + "/" + str(details.id)
        data = {"first_name": "TestchoEdit",
                "last_name": "TestchovEdit",
                "iban": "BG94 RZBB 9155 1060 3623 19",
                } | self.VALID_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(data["first_name"], resp.json["first_name"])
        self.assertEqual(data["last_name"], resp.json["last_name"])
        self.assertEqual(data["iban"].replace(" ", ""), resp.json["iban"])
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_image_url"])
        self.assertEqual(data["first_name"], details.first_name)
        self.assertEqual(data["last_name"], details.last_name)
        self.assertEqual(data["iban"].replace(" ", ""), details.iban)
        self.assertEqual(mocked_s3.return_value, details.profile_picture_image_url)

    @patch.object(s3, "upload_photo", return_value="some.s3.url")
    def test_change_profile_picture_with_valid_data_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        details = self._create_owner_details_in_test_db()

        url = self.URL + "/" + str(details.id)
        data = self.VALID_PHOTO_DATA

        resp = self.client.put(url, headers=self._HEADERS, json=data)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(mocked_s3.return_value, resp.json["profile_picture_image_url"])
        self.assertEqual(mocked_s3.return_value, details.profile_picture_image_url)

    @patch.object(s3, "delete_photo", return_value=None)
    def test_delete_existing_profile_picture_expect_status_200_cd_in_db_updated_correct_json(self, mocked_s3):
        data = self.SHOP_OWNER_DETAILS_DATA | {"profile_picture_image_url": "some.url"}

        details = self._create_owner_details_in_test_db(data)
        url = self.URL + "/" + str(details.id) + "/profile_picture"

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)

        self.assertEqual(200, resp.status_code)
        self.assertEqual(None, resp.json["profile_picture_image_url"])

    def test_delete_not_existing_profile_picture_expect_status_404_and_correct_message(self):
        details = self._create_owner_details_in_test_db()
        url = self.URL + "/" + str(details.id) + "/profile_picture"

        resp = self.client.delete(url, headers=self._AUTHORIZATION_HEADER)
        self.assertEqual(404, resp.status_code)

    def test_verify_information_admin_user_expect_200_and_change_in_db(self):
        admin = AdminFactory()
        token = generate_token(admin)
        headers = {"Authorization": f"Bearer {token}"} | self._HEADER_CONT_TYPE_JSON

        details = self._create_owner_details_in_test_db()

        url = self.URL + "/" + str(details.id) + "/verify"

        resp = self.client.put(url, headers=headers)

        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.json["verified"])
        self.assertTrue(details.verified)
