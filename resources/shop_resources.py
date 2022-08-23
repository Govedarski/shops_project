from flask import request
from werkzeug.exceptions import Forbidden

from managers.auth_manager import auth
from managers.crud_manager import CRUDManager
from managers.shop_manager import ShopManager
from models import ShopModel, UserRoles, AdminRoles
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateSchema, ValidateIsHolder, \
    ValidatePageExist
from resources.helpers.crud_resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin, \
    DeleteImageResourceMixin, GetListResourceMixin
from schemas.request.shop_schema_in import ShopCreateSchemaIn, ShopEditSchemaIn
from schemas.response.shop_schemas_out import ShopExtendedSchemaOut, ShopShortSchemaOut
from utils.resource_decorators import execute_access_validators


class ShopGetResourceMixin:
    def get_schema_out(self, **kwargs):
        """Shop all info to his holder and admins else short info"""
        instance = kwargs.get('instance')
        if self.is_current_user_admin() or self.is_current_user_holder(instance):
            return ShopExtendedSchemaOut
        return ShopShortSchemaOut

    @staticmethod
    def is_current_user_admin():
        user = auth.current_user()
        return user and user.role in AdminRoles

    @staticmethod
    def is_current_user_holder(instance):
        user = auth.current_user()
        return user and user.role != UserRoles.customer and user.id == instance.holder_id


class ShopResource(ShopGetResourceMixin, CreateResourceMixin, GetListResourceMixin):
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

    def get_manager(self):
        if request.method == "GET":
            return ShopManager
        return super().get_manager()


class ShopSingleResource(ShopGetResourceMixin, GetResourceMixin, EditResourceMixin):
    MODEL = ShopModel
    SCHEMA_IN = ShopEditSchemaIn
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_optional
    def get(self, pk):
        shop = CRUDManager.get(self.get_model(), pk)
        if shop.active or self.is_current_user_admin() or self.is_current_user_holder(shop):
            return self.get_schema_out(instance=shop)().dump(shop), 200
        raise Forbidden("Permission denied!")

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
        ValidateSchema()
    )
    def put(self, pk):
        return super().put(pk)


class ShopBrandPictureResource(DeleteImageResourceMixin):
    def delete(self, pk):
        return super().delete()