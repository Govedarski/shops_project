from resources.auth_resources import RegisterResource, LoginResource
from resources.customer_details_resources import CreateCustomerDetailsResource, CustomerDetailsResource, \
    CustomerProfilePictureResource, CreateShopOwnerDetailsResource, ShopOwnerDetailsResource

routes = (
    (RegisterResource, "/register"),
    (LoginResource, "/login"),

    # ("pass", "/customer"), # get all customer information TODO:later
    # ("pass", "/customer/delete"), # delete customer and all related details TODO: later
    # ("pass", "/customer/<:id>"),
    #
    (CreateCustomerDetailsResource, "/customer/details/create"),
    (CustomerDetailsResource, "/customer/details/<int:pk>"),
    (CustomerProfilePictureResource, "/customer/details/<int:pk>/profile_picture"),

    (CreateShopOwnerDetailsResource, "/shop_owner/details/create"),
    (ShopOwnerDetailsResource, "/shop_owner/details/<int:pk>"),
    # (ShopOwnerProfilePictureResource, "/shop_owner/details/<int:pk>/profile_picture"),
    # (ShopOwnerDocumentsResource, "/shop_owner/details/<int:pk>/documents"),

    # ("pass", "/customer/delivery_details"),
    # ("pass", "/customer/delivery_details/create"),
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
