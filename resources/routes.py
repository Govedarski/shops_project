from resources.auth_resources import RegisterResource, LoginResource, RegisterAdminResource
from resources.details_resources.customer_details_resources import CreateCustomerDetailsResource, \
    CustomerDetailsResource, CustomerProfilePictureResource
from resources.details_resources.delivery_address_resources import \
    DeliveryAddressDetailsResource, DeliveryAddressDetailsSingleResource
from resources.details_resources.shop_owner_details_resources import CreateShopOwnerDetailsResource, \
    ShopOwnerDetailsResource, ShopOwnerProfilePictureResource, VerifyShopOwnerDetailsResource
from resources.order_resources import OrderResource
from resources.product_rescources import ProductResource
from resources.shop_resources import ShopResource, ShopSingleResource, VerifyShopResource, BrandLogoResource, \
    DeactivateShopResource
from resources.webhook_resource import WebhookResource

routes = (
    (RegisterResource, "/users/register"),  # POST
    (RegisterAdminResource, "/admins/register"),  # POST
    (LoginResource, "/login"),  # POST

    # ("pass", "/customer/<:id>"),
    # ("pass", "/owner/<:id>"),
    # TODO: get with all related details_schemas_in delete with all related details_schemas_in if no order linked to it

    (CreateCustomerDetailsResource, "/customer_details"),  # POST
    (CustomerDetailsResource, "/customer_details/<int:pk>"),  # PUT, GET
    (CustomerProfilePictureResource, "/customer_details/<int:pk>/profile_picture"),  # DELETE

    (CreateShopOwnerDetailsResource, "/shop_owner_details"),  # POST
    (ShopOwnerDetailsResource, "/shop_owner_details/<int:pk>"),  # GET, PUT
    (VerifyShopOwnerDetailsResource, "/shop_owner_details/<int:pk>/verify"),  # PUT
    (ShopOwnerProfilePictureResource, "/shop_owner_details/<int:pk>/profile_picture"),  # put, DELETE

    (DeliveryAddressDetailsResource, "/delivery_address_details"),  # POST, GET
    (DeliveryAddressDetailsSingleResource, "/delivery_address_details/<int:pk>"),  # GET, PUT, DELETE

    (ShopResource, "/shops"),  # POST, GET
    (ShopSingleResource, "/shops/<int:pk>"),  # GET, PUT, DELETE
    (VerifyShopResource, "/shops/<int:pk>/verify"),  # PUT
    (DeactivateShopResource, "/shops/<int:pk>/deactivate"),  # PUT
    (BrandLogoResource, "/shops/<int:pk>/brand_logo"),  # DELETE

    (ProductResource, "/products"),  # POST - list of products, GET
    # (ShopSingleResource, "/products/<int:pk>"),  # GET, PUT, DELETE
    # (ProductPhotoResource, "/product/<int:pk>/photo"),  # DELETE

    (OrderResource, "/orders"),

    (WebhookResource, "/webhook")
)
