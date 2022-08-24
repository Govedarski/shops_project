from flask import request

from managers.auth_manager import auth
from managers.shop_manager import ShopManager
from models import UserRoles, AdminRoles
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateSchema
from resources.helpers.base_resources import VerifyBaseResource, RemoveImageBaseResource
from resources.helpers.resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin, \
    GetListResourceMixin, DeleteResourceMixin
from schemas.request.shop_schema_in import ShopCreateSchemaIn, ShopVerifiedEditSchemaIn, ShopNotVerifiedEditSchemaIn
from schemas.response.shop_schemas_out import ShopExtendedSchemaOut, ShopShortSchemaOut
from utils import helpers
from utils.resource_decorators import execute_access_validators


class ShopGetSchemaOutMixin:
    def get_schema_out(self, **kwargs):
        """Shop all info to his holder and admins else short info"""
        instance = kwargs.get('instance')
        user = auth.current_user()

        if helpers.is_admin(user) or helpers.is_holder(instance, UserRoles.owner, user):
            return ShopExtendedSchemaOut
        return ShopShortSchemaOut


class ShopResource(ShopGetSchemaOutMixin, CreateResourceMixin, GetListResourceMixin):
    MANAGER = ShopManager
    SCHEMA_IN = ShopCreateSchemaIn
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

    def filter_by(self):
        criteria = {}
        if request.query_string:
            queries = request.query_string.decode("utf-8").split("&")
            criteria = {field: criteria for field, criteria in [query.split("=") for query in queries]}

        return criteria


class ShopSingleResource(ShopGetSchemaOutMixin, GetResourceMixin, EditResourceMixin, DeleteResourceMixin):
    MANAGER = ShopManager
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_optional
    def get(self, pk):
        user = auth.current_user()
        return super().get(pk, user=user)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema()
    )
    def put(self, pk):
        current_user = auth.current_user()
        return super().put(pk, holder_required=True, user=current_user)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def delete(self, pk):
        current_user = auth.current_user()
        return super().delete(pk, holder_required=True, user=current_user)

    def get_schema_in(self, *args, **kwargs):
        pk = kwargs.get("pk")
        model = self.get_manager().get_model()
        obj = helpers.get_or_404(model, pk)
        return ShopVerifiedEditSchemaIn if obj.verified else ShopNotVerifiedEditSchemaIn


class BrandLogoResource(RemoveImageBaseResource):
    MANAGER = ShopManager
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "brand_logo"


class VerifyShopResource(VerifyBaseResource):
    MANAGER = ShopManager
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]

    def get_data(self):
        data = super().get_data()
        return data | {"active": True}


class DeactivateShopResource(EditResourceMixin):
    MANAGER = ShopManager
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def put(self, pk):
        return super().put(pk, holder_required=True, user=auth.current_user())

    def get_data(self):
        return {"active": False}
