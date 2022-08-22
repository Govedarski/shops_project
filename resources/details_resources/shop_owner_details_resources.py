from managers.auth_manager import auth
from models import ShopOwnerDetailsModel, UserRoles, AdminRoles
from resources.details_resources.base_details_resources import CreateDetailsResource, DetailsResource, \
    DetailsImageResource, RemoveIbanSpacesMixin
from schemas.request.details_schemas_in import CreateShopOwnerDetailsSchemaIn, EditShopOwnerDetailsSchemaIn
from schemas.response.details_schemas_out import ShopOwnerDetailsSchemaOut, DetailsSchemaOut


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


class ShopOwnerProfilePictureResource(DetailsImageResource):
    MODEL = ShopOwnerDetailsModel
    SCHEMA_OUT = DetailsSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "profile_picture"
    NOT_FOUND_MESSAGE = "Shop owner details not found!"
