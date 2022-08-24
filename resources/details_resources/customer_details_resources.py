from managers.details_managers.customer_details_manager import CustomerDetailsManager
from models import UserRoles, AdminRoles
from resources.details_resources.base_details_resources import CreateDetailsResource, DetailsResource
from resources.helpers.base_resources import RemoveImageBaseResource
from schemas.request.details_schemas_in.shop_owner_details_schemas_in import CreateDetailsSchemaIn, \
    EditDetailsSchemaIn
from schemas.response.details_schemas_out import DetailsSchemaOut


class CreateCustomerDetailsResource(CreateDetailsResource):
    MANAGER = CustomerDetailsManager
    SCHEMA_IN = CreateDetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]


class CustomerDetailsResource(DetailsResource):
    MANAGER = CustomerDetailsManager
    SCHEMA_IN = EditDetailsSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]


class CustomerProfilePictureResource(RemoveImageBaseResource):
    MANAGER = CustomerDetailsManager
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.customer, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"
    NOT_FOUND_MESSAGE = "Customer details_schemas_in not found!"
