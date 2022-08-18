from resources.auth_resources import RegisterResource, LoginResource
from resources.details_resources import CustomerDetailsResource, CreateCustomerDetailsResource, ProfilePictureResource

routes = (
    (RegisterResource, "/register"),
    (LoginResource, "/login"),

    # ("pass", "/customer"), # get all customer information TODO:later
    # ("pass", "/customer/delete"), # delete customer and all related details TODO: later
    # ("pass", "/customer/<:id>"),
    #
    (CreateCustomerDetailsResource, "/customer/details/create"),
    (CustomerDetailsResource, "/customer/details/<int:pk>"),
    (ProfilePictureResource, "/customer/details/<int:pk>/profile_picture"),

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
