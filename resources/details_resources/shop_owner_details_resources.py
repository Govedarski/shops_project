from managers.auth_manager import auth
from managers.details_managers.shop_owner_details_manager import ShopOwnerDetailsManager
from models import UserRoles, AdminRoles
from resources.details_resources.base_details_resources import CreateDetailsResource, DetailsResource, \
    RemoveIbanSpacesMixin
from resources.helpers.base_resources import VerifyBaseResource, RemoveImageBaseResource
from schemas.request.details_schemas_in.shop_owner_details_schemas_in import CreateShopOwnerDetailsSchemaIn, \
    EditShopOwnerDetailsSchemaIn
from schemas.response.details_schemas_out import ShopOwnerDetailsSchemaOut, DetailsSchemaOut


class CreateShopOwnerDetailsResource(RemoveIbanSpacesMixin, CreateDetailsResource):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_IN = CreateShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]


class ShopOwnerDetailsResource(RemoveIbanSpacesMixin, DetailsResource):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_IN = EditShopOwnerDetailsSchemaIn
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    def get_schema_out(self, **kwargs):
        current_user = auth.current_user()
        instance = kwargs.get('instance')
        if current_user == UserRoles.customer:
            return DetailsSchemaOut
        if current_user.role in AdminRoles or current_user.id == instance.holder_id:
            return ShopOwnerDetailsSchemaOut

        return DetailsSchemaOut


class ShopOwnerProfilePictureResource(RemoveImageBaseResource):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"


class VerifyShopOwnerDetailsResource(VerifyBaseResource):
    MANAGER = ShopOwnerDetailsManager
    SCHEMA_OUT = ShopOwnerDetailsSchemaOut
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]
