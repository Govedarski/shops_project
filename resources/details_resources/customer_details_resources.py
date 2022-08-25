from managers.auth_manager import auth
from managers.details_managers.customer_details_manager import CustomerDetailsManager
from models import UserRoles, AdminRoles
from resources.helpers.access_validators import ValidateRole, ValidateSchema
from resources.helpers.base_resources import RemoveImageBaseResource
from resources.helpers.resources_mixins import EditResourceMixin, CreateResourceMixin, GetResourceMixin
from schemas.request.details_schemas_in.base_details_schemas_in import DetailsSchemaIn, ChangeProfilePictureSchemaIn
from schemas.response.details_schemas_out import DetailsSchemaOut
from utils.decorators import execute_access_validators


class CreateCustomerDetailsResource(CreateResourceMixin):
    MANAGER = CustomerDetailsManager
    SCHEMA_IN = DetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema())
    def post(self):
        return super().post()


class CustomerDetailsResource(GetResourceMixin, EditResourceMixin):
    MANAGER = CustomerDetailsManager
    SCHEMA_IN = DetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    def get(self, pk, **kwargs):
        return super().get(pk, **kwargs)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema())
    def put(self, pk):
        current_user = auth.current_user()
        return super().put(pk, user=current_user, holder_required=True)


class CustomerProfilePictureResource(RemoveImageBaseResource, EditResourceMixin):
    MANAGER = CustomerDetailsManager
    SCHEMA_IN = ChangeProfilePictureSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def put(self, pk):
        current_user = auth.current_user()
        return super().put(pk, holder_required=True, user=current_user)
