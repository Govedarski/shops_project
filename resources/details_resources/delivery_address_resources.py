from managers.auth_manager import auth
from managers.details_managers.DeliveryAddressManager import DeliveryAddressDetailsManager
from managers.details_managers.customer_details_manager import CustomerDetailsManager
from models import AdminRoles, UserRoles
from resources.helpers.access_validators import ValidateRole, ValidateSchema
from resources.helpers.resources_mixins import CreateResourceMixin, GetListResourceMixin, \
    DeleteResourceMixin, EditResourceMixin, GetResourceMixin
from schemas.request.details_schemas_in.delivery_address_details_schemas_in import \
    AuthCreateDeliveryAddressDetailsSchemaIn, NoAuthCreateDeliveryAddressDetailsSchemaIn, \
    EditDeliveryAddressDetailsSchemaIn
from schemas.response.details_schemas_out import DeliveryAddressDetailsSchemaOut
from utils.decorators import execute_access_validators


class DeliveryAddressDetailsResource(CreateResourceMixin, GetListResourceMixin):
    MANAGER = DeliveryAddressDetailsManager
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
        return {}

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
        CustomerDetailsManager().create(
            {"first_name": data["first_name"],
             "last_name": data["last_name"]}
            , user)


class DeliveryAddressDetailsSingleResource(GetResourceMixin, EditResourceMixin, DeleteResourceMixin):
    MANAGER = DeliveryAddressDetailsManager
    SCHEMA_IN = EditDeliveryAddressDetailsSchemaIn
    SCHEMA_OUT = DeliveryAddressDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def get(self, pk):
        user = auth.current_user()
        return super().get(pk=pk, holder_required=True, user=user)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema())
    def put(self, pk):
        current_user = auth.current_user()
        return super().put(pk, user=current_user, holder_required=True)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def delete(self, pk):
        # TODO: If DAD is linked to order deleting forbidden
        user = auth.current_user()
        return super().delete(pk=pk, holder_required=True, user=user)
