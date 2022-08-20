from managers.auth_manager import auth
from models import CustomerDetailsModel, UserRoles, AdminRoles, ShopOwnerDetailsModel
from resources.access_endpoint_validators import ValidateRole, ValidateUniqueness, ValidateSchema, ValidatePageExist, \
    ValidateIsOwner
from resources.crud_resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin, \
    DeleteImageResourceMixin
from schemas.request.details_schemas_in import CreateDetailsSchemaIn, \
    CreateShopOwnerDetailsSchemaIn, EditShopOwnerDetailsSchemaIn, EditDetailsSchemaIn
from schemas.response.details_schemas_out import DetailsSchemaOut, ShopOwnerDetailsSchemaOut
from utils.resource_decorators import execute_access_validators


class CreateDetailsResource(CreateResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateUniqueness(),
        ValidateSchema()
    )
    def post(self):
        return super().post()


class DetailsResource(GetResourceMixin, EditResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidatePageExist()
    )
    def get(self, pk):
        return super().get(pk)

    @auth.login_required
    @execute_access_validators(
        ValidatePageExist(),
        ValidateRole(),
        ValidateIsOwner(),
        ValidateSchema()
    )
    def put(self, pk):
        return super().put(pk)


class DetailsImageResource(DeleteImageResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidatePageExist(),
        ValidateRole(),
        ValidateIsOwner(),
    )
    def delete(self, pk):
        return super().delete(pk)


class RemoveIbanSpacesMixin:
    def get_data(self):
        data = super().get_data()
        if hasattr(data, "iban"):
            data["iban"] = data["iban"].replace(" ", "")

        return data


class CreateCustomerDetailsResource(CreateDetailsResource):
    MODEL = CustomerDetailsModel
    SCHEMA_IN = CreateDetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]


class CustomerDetailsResource(DetailsResource):
    MODEL = CustomerDetailsModel
    SCHEMA_IN = EditDetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]
    NOT_FOUND_MESSAGE = "Customer details not found!"


class CustomerProfilePictureResource(DetailsImageResource):
    MODEL = CustomerDetailsModel
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"
    NOT_FOUND_MESSAGE = "Customer details not found!"


class CreateShopOwnerDetailsResource(RemoveIbanSpacesMixin, CreateDetailsResource):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_IN = CreateShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]


class ShopOwnerDetailsResource(RemoveIbanSpacesMixin, DetailsResource):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_IN = EditShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    NOT_FOUND_MESSAGE = "Shop owner details not found!"


class ShopOwnerProfilePictureResource(DetailsImageResource):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"
    NOT_FOUND_MESSAGE = "Shop owner details not found!"
