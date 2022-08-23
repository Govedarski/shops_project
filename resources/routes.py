from resources.auth_resources import RegisterResource, LoginResource, RegisterAdminResource
from resources.details_resources.customer_details_resources import CreateCustomerDetailsResource, \
    CustomerDetailsResource, CustomerProfilePictureResource
from resources.details_resources.delivery_address_resources import \
    DeliveryAddressDetailsResource, DeliveryAddressDetailsSingleResource
from resources.details_resources.shop_owner_details_resources import CreateShopOwnerDetailsResource, \
    ShopOwnerDetailsResource, ShopOwnerProfilePictureResource, VerifyShopOwnerDetailsResource
from resources.shop_resources import ShopResource, ShopSingleResource, VerifyShopResource, BrandLogoResource, \
    DeactivateShopResource

routes = (
    (RegisterResource, "/register"),  # POST
    (RegisterAdminResource, "/admin/register"),  # POST
    (LoginResource, "/login"),  # POST

    # ("pass", "/customer/<:id>"),
    # ("pass", "/owner/<:id>"),
    # (pass, "/shop/<int:pk>/products"),
    # TODO: get with all related details_schemas_in delete with all related details_schemas_in if no order linked to it

    (CreateCustomerDetailsResource, "/customer/details"),  # POST
    (CustomerDetailsResource, "/customer/details/<int:pk>"),  # GET, PUT
    (CustomerProfilePictureResource, "/customer/details/<int:pk>/profile_picture"),  # DELETE

    (CreateShopOwnerDetailsResource, "/shop_owner/details"),  # POST
    (ShopOwnerDetailsResource, "/shop_owner/details/<int:pk>"),  # GET, PUT
    (VerifyShopOwnerDetailsResource, "/shop_owner/details/<int:pk>/verify"),  # PUT
    (ShopOwnerProfilePictureResource, "/shop_owner/details/<int:pk>/profile_picture"),  # DELETE

    (DeliveryAddressDetailsResource, "/delivery_address_details"),  # POST, GET
    (DeliveryAddressDetailsSingleResource, "/delivery_address_details/<int:pk>"),  # GET, PUT, DELETE

    (ShopResource, "/shop"),  # POST, GET
    (ShopSingleResource, "/shop/<int:pk>"),  # GET, PUT, DELETE
    (VerifyShopResource, "/shop/<int:pk>/verify"),  # PUT
    (DeactivateShopResource, "/shop/<int:pk>/deactivate"),  # PUT
    (BrandLogoResource, "/shop/<int:pk>/brand_logo"),  # DELETE

    # (ShopResource, "/product"),  # POST - list of products, GET
    # (ShopSingleResource, "/product/<int:pk>"),  # GET, PUT, DELETE
    # (VerifyShopResource, "/product/<int:pk>/listed"),  # PUT
    # (ProductPhotoResource, "/product/<int:pk>/photo"),  # DELETE
)
