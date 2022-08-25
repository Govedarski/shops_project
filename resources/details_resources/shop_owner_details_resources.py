from managers.auth_manager import auth
from managers.details_managers.shop_owner_details_manager import ShopOwnerDetailsManager
from models import UserRoles, AdminRoles
from resources.helpers.access_validators import ValidateRole, ValidateSchema
from resources.helpers.base_resources import VerifyBaseResource, RemoveImageBaseResource
from resources.helpers.resources_mixins import EditResourceMixin, CreateResourceMixin, GetResourceMixin, \
    RemoveIbanSpacesMixin
from schemas.request.details_schemas_in.base_details_schemas_in import ChangeProfilePictureSchemaIn
from schemas.request.details_schemas_in.shop_owner_details_schemas_in import ShopOwnerDetailsSchemaIn
from schemas.response.details_schemas_out import ShopOwnerDetailsSchemaOut, DetailsSchemaOut
from utils.decorators import execute_access_validators


class CreateShopOwnerDetailsResource(RemoveIbanSpacesMixin, CreateResourceMixin):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_IN = ShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema())
    def post(self):
        return super().post()


class ShopOwnerDetailsResource(RemoveIbanSpacesMixin, GetResourceMixin, EditResourceMixin):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_IN = ShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

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

    def get_schema_out(self, **kwargs):
        current_user = auth.current_user()
        instance = kwargs.get('instance')
        if current_user == UserRoles.customer:
            return DetailsSchemaOut
        if current_user.role in AdminRoles or current_user.id == instance.holder_id:
            return ShopOwnerDetailsSchemaOut

        return DetailsSchemaOut


class ShopOwnerProfilePictureResource(RemoveImageBaseResource, EditResourceMixin):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_IN = ChangeProfilePictureSchemaIn
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def put(self, pk):
        current_user = auth.current_user()
        return super().put(pk, holder_required=True, user=current_user)


class VerifyShopOwnerDetailsResource(VerifyBaseResource):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]
