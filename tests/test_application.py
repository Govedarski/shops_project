from managers.auth_manager import AuthManager
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateIsHolder
from tests.base_test_case import BaseTestCase
from tests.factories import CustomerFactory, OwnerFactory, AdminFactory, SuperAdminFactory
from tests.helpers import generate_token


class TestApp(BaseTestCase):
    ENDPOINTS_DATA = (
        ("/admin/register", "post"),
        ("/customer/details", "post"),
        ("/customer/details/1", "get"),
        ("/customer/details/1", "put"),
        ("/customer/details/1/profile_picture", "delete"),
        ("/shop_owner/details", "post"),
        ("/shop_owner/details/1", "put"),
        ("/shop_owner/details/1", "get"),
        ("/shop_owner/details/1/verify", "put"),
        ("/shop_owner/details/1/profile_picture", "delete"),
        ("delivery_address_details", "get"),
        ("delivery_address_details/1", "get"),
        ("delivery_address_details/1", "put"),
        ("delivery_address_details/1", "delete"),
        ("shop", "post"),
        ("shop/1", "put"),
        ("shop/1/verify", "put"),
        ("/shop/1/brand_logo", "delete"),

    )

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

        for url, method in endpoints_data:
            request = getattr(self.client, method)
            resp = request(url, headers=headers)
            print(f"Testing: {url}")
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
            self.ENDPOINTS_DATA,
            self.assert_401,
            expected_resp_body={"message": AuthManager.MISSING_TOKEN_MESSAGE}
        )

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer Invalid Token"}
        self._iterate_endpoints(
            self.ENDPOINTS_DATA,
            self.assert_401,
            expected_resp_body={"message": AuthManager.INVALID_TOKEN_MESSAGE},
            headers=headers
        )

    def test_missing_permissions_for_admin_raises(self):
        endpoints = (
            ("/admin/register", "post"),
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
            ("/admin/register", "post"),
            ("/shop_owner/details", "post"),
            ("/shop_owner/details/1", "put"),
            ("/shop_owner/details/1/verify", "put"),
            ("/shop_owner/details/1/profile_picture", "delete"),
            ("/shop", "post"),
            ("shop/1", "put"),
            ("/shop/1/verify", "put"),
            ("/shop/1/brand_logo", "delete"),
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
            ("/admin/register", "post"),
            ("/customer/details", "post"),
            ("/customer/details/1", "put"),
            ("/customer/details/1/profile_picture", "delete"),
            ("/delivery_address_details", "post"),
            ("/delivery_address_details", "get"),
            ("/delivery_address_details/1", "put"),
            ("/delivery_address_details/1", "get"),
            ("/delivery_address_details/1", "delete"),
            ("/shop_owner/details/1/verify", "put"),
            ("/shop/1/verify", "put"),

        )
        user = OwnerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateRole.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    def test_missing_permissions_for_not_holder_customer_raises(self):
        endpoints = (
            ("/customer/details/1", "put"),
            ("/customer/details/1/profile_picture", "delete"),
            ("/delivery_address_details/1", "put"),
            ("/delivery_address_details/1", "get"),
            ("/delivery_address_details/1", "delete"),
            ("shop/1", "put"),
        )

        user = CustomerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateIsHolder.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    def test_missing_permissions_for_not_holder_shop_owner_raises(self):
        endpoints = (
            ("/shop_owner/details/1", "put"),
            ("/shop_owner/details/1/profile_picture", "delete"),
            ("shop/1", "put"),
            ("/shop/1/brand_logo", "delete"),

        )
        user = OwnerFactory()

        self._iterate_endpoints(
            endpoints,
            self.assert_403,
            expected_resp_body={"message": ValidateRole.ERROR_MESSAGE},
            headers=self._crate_auth_header(user)
        )

    def test_page_not_found_raises(self):
        endpoints = (
            ("/customer/details/1", "get"),
            ("/customer/details/1", "put"),
            ("/customer/details/1/profile_picture", "delete"),
            ("/shop_owner/details/1", "get"),
            ("/shop_owner/details/1", "put"),
            ("/shop_owner/details/1/profile_picture", "delete"),
            ("/shop_owner/details/1/verify", "put"),
            ("/delivery_address_details/1", "get"),
            ("/delivery_address_details/1", "put"),
            ("/delivery_address_details/1", "delete"),
            ("shop/1", "put"),

        )
        user = SuperAdminFactory()
        self._iterate_endpoints(
            endpoints,
            self.assert_404,
            headers=self._crate_auth_header(user)
        )
