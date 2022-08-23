from flask import request

from managers.auth_manager import auth
from managers.shop_manager import ShopManager
from models import ShopModel, UserRoles, AdminRoles
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateSchema, ValidateIsHolder, \
    ValidatePageExist
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
    MODEL = ShopModel
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
    MODEL = ShopModel
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_optional
    @execute_access_validators(
        ValidatePageExist(),
    )
    def get(self, pk):
        user = auth.current_user()
        return super().get(pk, user=user)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
        ValidateSchema()
    )
    def put(self, pk):
        return super().put(pk)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def delete(self, pk):
        return super().delete(pk)

    def get_schema_in(self, *args, **kwargs):
        # get object always returns shop because page exist validation is past
        pk = kwargs.get("pk")
        return ShopVerifiedEditSchemaIn if self.get_object(pk).verified else ShopNotVerifiedEditSchemaIn


class BrandLogoResource(RemoveImageBaseResource):
    MANAGER = ShopManager
    MODEL = ShopModel
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]
    IMAGE_FIELD_NAME = "brand_logo"


class VerifyShopResource(VerifyBaseResource):
    MANAGER = ShopManager
    MODEL = ShopModel
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]

    def get_data(self):
        data = super().get_data()
        return data | {"active": True}


class DeactivateShopResource(EditResourceMixin):
    MANAGER = ShopManager
    MODEL = ShopModel
    SCHEMA_OUT = ShopExtendedSchemaOut
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def put(self, pk):
        return super().put(pk)

    def get_data(self):
        return {"active": False}
