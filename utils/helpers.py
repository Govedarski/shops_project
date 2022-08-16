from werkzeug.exceptions import BadRequest

from models import UserRoles, CustomerModel, ShopOwnerModel


def get_user_model(role):
    if role == UserRoles.customer.name:
        return CustomerModel
    elif role == UserRoles.owner.name:
        return ShopOwnerModel
    else:
        raise BadRequest("Invalid user role!")
