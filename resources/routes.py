from resources.auth_resources import RegisterResource, LoginResource, RegisterAdminResource
from resources.details_resources.customer_details_resources import CreateCustomerDetailsResource, \
    CustomerDetailsResource, CustomerProfilePictureResource
from resources.details_resources.delivery_address_resources import VerifyShopOwnerDetailsResource, \
    DeliveryAddressDetailsResource, SingleDeliveryAddressDetailsResource
from resources.details_resources.shop_owner_details_resources import CreateShopOwnerDetailsResource, \
    ShopOwnerDetailsResource, ShopOwnerProfilePictureResource

routes = (
    (RegisterResource, "/register"),  # POST
    (RegisterAdminResource, "/admin/register"),  # POST
    (LoginResource, "/login"),  # POST

    # ("pass", "/customer"), # get all customer information TODO:later
    # ("pass", "/customer/delete"), # delete customer and all related details TODO: later
    # ("pass", "/customer/<:id>"),
    #
    (CreateCustomerDetailsResource, "/customer/details"),  # POST
    (CustomerDetailsResource, "/customer/details/<int:pk>"),  # GET, PUT
    (CustomerProfilePictureResource, "/customer/details/<int:pk>/profile_picture"),  # DELETE

    (CreateShopOwnerDetailsResource, "/shop_owner/details"),  # POST
    (ShopOwnerDetailsResource, "/shop_owner/details/<int:pk>"),  # GET, PUT
    (VerifyShopOwnerDetailsResource, "/shop_owner/details/<int:pk>/verify"),  # PUT
    (ShopOwnerProfilePictureResource, "/shop_owner/details/<int:pk>/profile_picture"),  # DELETE

    (DeliveryAddressDetailsResource, "/delivery_address_details"),  # POST, GET
    (SingleDeliveryAddressDetailsResource, "/delivery_address_details/<int:pk>"),  # GET, PUT, DELETE
    # (GetAllDeliveryAddressDetailsResource, "/delivery_address_details/"),

    # ("pass", "/customer/delivery_details/create"),

    # ("pass", "/customer/delivery_details"),
    # ("pass", "/customer/delivery_details/edit"),
    # ("pass", "/customer/delivery_details/delete"),
    #
    # ("pass", "/owner"),  # get all owner information TODO: later
    # ("pass", "/owner/<:id>"),
    # ("pass", "/owner/delete"),  # delete owner and all related details TODO: later

    # ("pass", "/owner/details"),
    # ("pass", "/owner/details/create"),
    # ("pass", "/owner/details/edit")

    # ("pass", "/owner/shop/create"),
    # ("pass", "/owner/shop/edit"),
    # ("pass", "/owner/shop/delete")

    # ("pass", "/shop/list"),
    # ("pass", "/shop/<:id>"),

    # ("pass", "/admin/category/create"),
)
