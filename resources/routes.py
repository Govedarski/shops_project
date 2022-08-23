from resources.auth_resources import RegisterResource, LoginResource, RegisterAdminResource
from resources.details_resources.customer_details_resources import CreateCustomerDetailsResource, \
    CustomerDetailsResource, CustomerProfilePictureResource
from resources.details_resources.delivery_address_resources import VerifyShopOwnerDetailsResource, \
    DeliveryAddressDetailsResource, DeliveryAddressDetailsSingleResource
from resources.details_resources.shop_owner_details_resources import CreateShopOwnerDetailsResource, \
    ShopOwnerDetailsResource, ShopOwnerProfilePictureResource
from resources.shop_resources import ShopResource, ShopSingleResource

routes = (
    (RegisterResource, "/register"),  # POST
    (RegisterAdminResource, "/admin/register"),  # POST
    (LoginResource, "/login"),  # POST

    # ("pass", "/customer/<:id>"),
    # ("pass", "/owner/<:id>"),
    # TODO: get with all related details_schemas_in delete with all related details_schemas_in if no order linked to it

    (CreateCustomerDetailsResource, "/customer/details_schemas_in"),  # POST
    (CustomerDetailsResource, "/customer/details_schemas_in/<int:pk>"),  # GET, PUT
    (CustomerProfilePictureResource, "/customer/details_schemas_in/<int:pk>/profile_picture"),  # DELETE

    (CreateShopOwnerDetailsResource, "/shop_owner/details_schemas_in"),  # POST
    (ShopOwnerDetailsResource, "/shop_owner/details_schemas_in/<int:pk>"),  # GET, PUT
    (VerifyShopOwnerDetailsResource, "/shop_owner/details_schemas_in/<int:pk>/verify"),  # PUT
    (ShopOwnerProfilePictureResource, "/shop_owner/details_schemas_in/<int:pk>/profile_picture"),  # DELETE

    (DeliveryAddressDetailsResource, "/delivery_address_details"),  # POST, GET
    (DeliveryAddressDetailsSingleResource, "/delivery_address_details/<int:pk>"),  # GET, PUT, DELETE

    (ShopResource, "/shop"),  # POST, GET
    (ShopSingleResource, "/shop/<int:pk>"),  # GET, PUT

    # # TODO
    # (VerifyShopOwnerDetailsResource, "/shop/<int:pk>/verify"),  # PUT
    # (VerifyShopOwnerDetailsResource, "/shop/<int:pk>/deactivate"),  # PUT
    # (ShopBrandPictureResource, "/shop/details_schemas_in/<int:pk>/profile_picture"),  # DELETE

)
