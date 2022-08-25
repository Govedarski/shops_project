from managers.auth_manager import auth
from managers.details_managers.product_manager import ProductManager
from models import UserRoles, AdminRoles
from resources.helpers.access_validators import ValidateRole, ValidateSchema
from resources.helpers.resources_mixins import CreateResourceMixin, GetListResourceMixin
from schemas.request.product_schemas_in import ProductSchemaIn
from utils.decorators import execute_access_validators


class ProductResource(CreateResourceMixin, GetListResourceMixin):
    MANAGER = ProductManager
    SCHEMA_IN = ProductSchemaIn
    # SCHEMA_OUT = ProductSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema(),
    )
    def post(self):
        return super().post()

    @auth.login_optional
    def get(self):
        user = auth.current_user()
        return super().get(user=user)
