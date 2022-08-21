from managers.auth_manager import auth
from models import CustomerDetailsModel, UserRoles, AdminRoles, ShopOwnerDetailsModel, DeliveryAddressDetailsModel
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateUniqueness, ValidateSchema, \
    ValidatePageExist, \
    ValidateIsOwner
from resources.helpers.crud_resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin, \
    DeleteImageResourceMixin
from schemas.request.details_schemas_in import CreateDetailsSchemaIn, \
    CreateShopOwnerDetailsSchemaIn, EditShopOwnerDetailsSchemaIn, EditDetailsSchemaIn, \
    AuthCreateDeliveryAddressDetailsSchemaIn, NoAuthCreateDeliveryAddressDetailsSchemaIn
from schemas.response.details_schemas_out import DetailsSchemaOut, ShopOwnerDetailsSchemaOut, \
    DeliveryAddressDetailsSchemaOut
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
        iban = data.get("iban")
        if iban:
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

    def get_schema_out(self, **kwargs):
        current_user = auth.current_user()
        pk = kwargs.get('pk')
        shop_owner_details = self.get_model().query.filter_by(id=pk).first()
        if current_user.role in AdminRoles or current_user.id == shop_owner_details.holder_id:
            return ShopOwnerDetailsSchemaOut

        return DetailsSchemaOut


class VerifyShopOwnerDetailsResource(EditResourceMixin):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidatePageExist(),
        ValidateRole(),
    )
    def put(self, pk):
        result = super().put(pk)
        if result[1] == 200:
            return {"verified": True}, 200
        return result

    def get_data(self):
        return {"verified": True}


class ShopOwnerProfilePictureResource(DetailsImageResource):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"
    NOT_FOUND_MESSAGE = "Shop owner details not found!"


class CreateDeliveryAddressDetailsResource(CreateResourceMixin):
    MODEL = DeliveryAddressDetailsModel
    SCHEMA_OUT = DeliveryAddressDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer]

    @auth.login_optional
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema(),
    )
    def post(self):
        return super().post()

    def get_schema_in(self):
        current_user = auth.current_user()
        if current_user:
            return AuthCreateDeliveryAddressDetailsSchemaIn
        return NoAuthCreateDeliveryAddressDetailsSchemaIn

    def get_data(self):
        data = super().get_data()
        current_user = auth.current_user()
        if current_user:
            data['first_name'] = current_user.details.first_name
            data['last_name'] = current_user.details.last_name
        return data
