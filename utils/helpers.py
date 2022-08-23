import base64
import uuid

from werkzeug.exceptions import BadRequest, NotFound

from models import UserRoles, CustomerModel, ShopOwnerModel, AdminRoles, AdminModel


def get_user_model(role):
    if role == UserRoles.customer.name:
        return CustomerModel
    elif role == UserRoles.owner.name:
        return ShopOwnerModel
    else:
        raise BadRequest("Invalid user role!")


def get_user_or_admin_model(role):
    if role in AdminRoles.__members__.keys():
        return AdminModel
    return get_user_model(role)


def is_admin(user):
    return user and user.role in AdminRoles


def is_holder(instance, holder_role, user):
    return user and user.role == holder_role and user.id == instance.holder_id


def get_or_404(model, pk, message=None):
    if not message:
        message = "Page not found!"

    instance = model.query.filter_by(id=pk).first()
    if not instance:
        raise NotFound(message)


def decode_file(encoded_file):
    return base64.b64decode(encoded_file.encode("utf-8"))


def save_file(path, file):
    with open(path, "wb") as f:
        f.write(file)


def create_photo_from_json(photo_str, extension):
    file_name = f"{str(uuid.uuid4())}.{extension}"
    return file_name, decode_file(photo_str)


def has_photo(photo_str, extension):
    if not photo_str and extension:
        raise BadRequest("There is not photo provided!")
    elif photo_str and not extension:
        raise BadRequest("There is not extension provided!")
    elif not photo_str and not extension:
        return False
    return True


def get_photo_name_by_url(photo_url):
    try:
        return photo_url.split("/")[-1]
    except AttributeError:
        return None
