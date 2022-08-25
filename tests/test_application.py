from unittest.mock import patch

from managers.auth_manager import AuthManager
from resources.helpers.access_validators import ValidateRole, ValidateSchema
from resources.helpers.resources_mixins import RemoveIbanSpacesMixin
from tests.base_test_case import BaseTestCase
from tests.constants import Endpoints
from tests.factories import CustomerFactory, OwnerFactory, AdminFactory, SuperAdminFactory
from tests.helpers import generate_token


class TestApp(BaseTestCase):
    LOGIN_REQUIRED_ENDPOINTS = (
        Endpoints.REGISTER_ADMIN,
        Endpoints.CREATE_CUSTOMER_DETAILS,
        Endpoints.GET_CUSTOMER_DETAILS,
        Endpoints.EDIT_CUSTOMER_DETAILS,
        Endpoints.DELETE_CUSTOMER_PROFILE_PICTURE,
        Endpoints.CREATE_SHOP_OWNER_DETAILS,
        Endpoints.GET_SHOP_OWNER_DETAILS,
        Endpoints.EDIT_SHOP_OWNER_DETAILS,
        Endpoints.VERIFY_SHOP_OWNER_DETAILS,
        Endpoints.DELETE_SHOP_OWNER_PROFILE_PICTURE,
        Endpoints.GET_LIST_DELIVERY_ADDRESS,
        Endpoints.GET_DELIVERY_ADDRESS,
        Endpoints.EDIT_DELIVERY_ADDRESS,
        Endpoints.DELETE_DELIVERY_ADDRESS,
        Endpoints.CREATE_SHOP,
        Endpoints.EDIT_SHOP,
        Endpoints.DELETE_SHOP,
        Endpoints.VERIFY_SHOP,
        Endpoints.DEACTIVATE_SHOP,
        Endpoints.DELETE_SHOP_BRAND_LOGO,
    )

    class MockedInstance(object):
        holder_id = None

    def setUp(self):
        super().setUp()

    def _iterate_endpoints(
            self,
            endpoints_data,
            status_code_method,
            expected_resp_body=None,
            headers=None,
    ):
        if not headers:
            headers = {}

        for endpoint in endpoints_data:
            url, method = endpoint
            print(f"Testing: {endpoint}")
            request = getattr(self.client, method)
            resp = request(url.replace("<int:pk>", "1"), headers=headers)
            status_code_method(resp)
            if expected_resp_body:
                self.assertEqual(resp.json, expected_resp_body)
            print(f"Done!")

    @staticmethod
    def _crate_auth_header(user):
        token = generate_token(user)
        return {"Authorization": f"Bearer {token}"}

    def test_login_required(self):
        self._iterate_endpoints(
            self.LOGIN_REQUIRED_ENDPOINTS,
            self.assert_401,
            expected_resp_body={"message": AuthManager.MISSING_TOKEN_MESSAGE}
        )

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer Invalid Token"}
        self._iterate_endpoints(
            self.LOGIN_REQUIRED_ENDPOINTS,
            self.assert_401,
            expected_resp_body={"message": AuthManager.INVALID_TOKEN_MESSAGE},
            headers=headers
        )

    def test_missing_permissions_for_admin_raises(self):
        endpoints = (
            Endpoints.REGISTER_ADMIN,
        )
        user = AdminFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateRole.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    def test_missing_permissions_for_customer_raises(self):
        endpoints = (
            Endpoints.REGISTER_ADMIN,
            Endpoints.CREATE_SHOP_OWNER_DETAILS,
            Endpoints.EDIT_SHOP_OWNER_DETAILS,
            Endpoints.VERIFY_SHOP_OWNER_DETAILS,
            Endpoints.DELETE_SHOP_OWNER_PROFILE_PICTURE,
            Endpoints.CREATE_SHOP,
            Endpoints.EDIT_SHOP,
            Endpoints.DELETE_SHOP,
            Endpoints.VERIFY_SHOP,
            Endpoints.DELETE_SHOP_BRAND_LOGO,
            Endpoints.DEACTIVATE_SHOP
        )
        user = CustomerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateRole.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    def test_missing_permissions_for_shop_owner_raises(self):
        endpoints = (
            Endpoints.REGISTER_ADMIN,
            Endpoints.CREATE_CUSTOMER_DETAILS,
            Endpoints.EDIT_CUSTOMER_DETAILS,
            Endpoints.DELETE_CUSTOMER_PROFILE_PICTURE,
            Endpoints.CREATE_DELIVERY_ADDRESS,
            Endpoints.GET_LIST_DELIVERY_ADDRESS,
            Endpoints.EDIT_DELIVERY_ADDRESS,
            Endpoints.GET_DELIVERY_ADDRESS,
            Endpoints.DELETE_DELIVERY_ADDRESS,
            Endpoints.VERIFY_SHOP_OWNER_DETAILS,
            Endpoints.VERIFY_SHOP,

        )
        user = OwnerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateRole.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    @patch("utils.helpers.get_or_404", return_value=MockedInstance)
    @patch.object(ValidateSchema, "validate", return_value=True)
    def test_missing_permissions_for_not_holder_raises(self, mock_page_exist, mocked_validation):
        endpoints = (
            Endpoints.EDIT_CUSTOMER_DETAILS,
            Endpoints.DELETE_CUSTOMER_PROFILE_PICTURE,
            Endpoints.EDIT_SHOP_OWNER_DETAILS,
            Endpoints.DELETE_SHOP_OWNER_PROFILE_PICTURE,
            Endpoints.GET_DELIVERY_ADDRESS,
            Endpoints.EDIT_DELIVERY_ADDRESS,
            Endpoints.DELETE_DELIVERY_ADDRESS,
            Endpoints.EDIT_SHOP,
            Endpoints.DELETE_SHOP,
            Endpoints.DEACTIVATE_SHOP,
            Endpoints.DELETE_SHOP_BRAND_LOGO,
        )

        user = CustomerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": "Permission denied!"},
            headers=self._crate_auth_header(user)
        )

    @patch.object(ValidateSchema, "validate", return_value=True)
    @patch.object(RemoveIbanSpacesMixin, "get_data", return_value=None)
    def test_page_not_found_raises(self, mock_validation, mocked_data):
        endpoints = (
            Endpoints.GET_CUSTOMER_DETAILS,
            Endpoints.EDIT_CUSTOMER_DETAILS,
            Endpoints.DELETE_CUSTOMER_PROFILE_PICTURE,
            Endpoints.GET_SHOP_OWNER_DETAILS,
            Endpoints.EDIT_SHOP_OWNER_DETAILS,
            Endpoints.VERIFY_SHOP_OWNER_DETAILS,
            Endpoints.DELETE_SHOP_OWNER_PROFILE_PICTURE,
            Endpoints.GET_DELIVERY_ADDRESS,
            Endpoints.EDIT_DELIVERY_ADDRESS,
            Endpoints.DELETE_DELIVERY_ADDRESS,
            Endpoints.EDIT_SHOP,
            Endpoints.DELETE_SHOP,
            Endpoints.VERIFY_SHOP,
            Endpoints.DEACTIVATE_SHOP,
            Endpoints.DELETE_SHOP_BRAND_LOGO,
        )
        admin = SuperAdminFactory()
        self._iterate_endpoints(
            endpoints,
            self.assert_404,
            headers=self._crate_auth_header(admin)
        )
