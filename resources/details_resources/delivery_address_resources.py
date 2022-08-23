from managers.auth_manager import auth
from managers.crud_manager import CRUDManager
from models import AdminRoles, DeliveryAddressDetailsModel, UserRoles, CustomerDetailsModel
from resources.details_resources.base_details_resources import DetailsResource
from resources.helpers.access_endpoint_validators import ValidatePageExist, ValidateRole, ValidateSchema, \
    ValidateIsHolder
from resources.helpers.resources_mixins import CreateResourceMixin, GetListResourceMixin, \
    DeleteResourceMixin
from schemas.request.details_schemas_in.delivery_address_details_schemas_in import \
    AuthCreateDeliveryAddressDetailsSchemaIn, NoAuthCreateDeliveryAddressDetailsSchemaIn, \
    EditDeliveryAddressDetailsSchemaIn
from schemas.response.details_schemas_out import DeliveryAddressDetailsSchemaOut
from utils.resource_decorators import execute_access_validators


class DeliveryAddressDetailsResource(CreateResourceMixin, GetListResourceMixin):
    MODEL = DeliveryAddressDetailsModel
    SCHEMA_OUT = DeliveryAddressDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer]

    @auth.login_optional
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema(),
    )
    def post(self):
        result = super().post()
        current_user = auth.current_user()
        if current_user and current_user.role == UserRoles.customer and not current_user.details:
            self._create_customer_details(current_user)
        return result

    @auth.login_required
    @execute_access_validators(
        ValidateRole([UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]),
    )
    def get(self):
        return super().get()

    def filter_by(self):
        current_user = auth.current_user()
        if current_user.role == UserRoles.customer:
            return {"holder_id": current_user.id}
        return None

    def get_schema_in(self):
        current_user = auth.current_user()
        if current_user and current_user.details:
            return AuthCreateDeliveryAddressDetailsSchemaIn
        return NoAuthCreateDeliveryAddressDetailsSchemaIn

    def get_data(self):
        data = super().get_data()
        current_user = auth.current_user()
        if current_user and current_user.details:
            data['first_name'] = current_user.details.first_name
            data['last_name'] = current_user.details.last_name
        return data

    def _create_customer_details(self, user):
        data = self.get_data()
        CRUDManager.create(CustomerDetailsModel,
                           {"first_name": data["first_name"],
                            "last_name": data["last_name"]}, user)


class DeliveryAddressDetailsSingleResource(DetailsResource, DeleteResourceMixin):
    MODEL = DeliveryAddressDetailsModel
    SCHEMA_IN = EditDeliveryAddressDetailsSchemaIn
    SCHEMA_OUT = DeliveryAddressDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]
    NOT_FOUND_MESSAGE = "Delivery address details_schemas_in not found!"

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def get(self, pk):
        return super().get(pk=pk)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def delete(self, pk):
        # TODO: If DAD is linked to order deleting forbidden
        return super().delete(pk=pk)
