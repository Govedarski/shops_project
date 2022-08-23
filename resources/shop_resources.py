from flask import request
from werkzeug.exceptions import NotFound

from managers.auth_manager import auth
from models import ShopModel, UserRoles, AdminRoles
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateSchema, ValidateIsHolder, \
    ValidatePageExist
from resources.helpers.crud_resources_mixins import CreateResourceMixin, GetListResourceMixin, \
    GetResourceMixin, EditResourceMixin, DeleteImageResourceMixin
from schemas.request.shop_schema_in import ShopCreateSchemaIn, ShopEditSchemaIn
from schemas.response.shop_schemas_out import ShopExtendedSchemaOut, ShopShortSchemaOut
from utils.resource_decorators import execute_access_validators


class ShopResource(CreateResourceMixin, GetListResourceMixin):
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
        return super().get()

    def filter_by(self):
        # show not active shops only to admins and their owners
        criteria = {}
        if request.query_string:
            queries = request.query_string.decode("utf-8").split("&")
            criteria = {field: criteria for field, criteria in [query.split("=") for query in queries]}

        current_user = auth.current_user()
        if not current_user or current_user.role == UserRoles.customer:
            return criteria | {"active": True}

        if current_user.role in AdminRoles or current_user.id == criteria.get("holder_id"):
            return criteria

        return criteria | {"active": True}

    def get_schema_out(self, *args, **kwargs):
        current_user = auth.current_user()
        instance = kwargs.get('instance')
        if current_user and (current_user.role in AdminRoles or current_user.id == instance.holder_id):
            return ShopExtendedSchemaOut

        return ShopShortSchemaOut


class ShopSingleResource(GetResourceMixin, EditResourceMixin):
    MODEL = ShopModel
    SCHEMA_IN = ShopEditSchemaIn
    ALLOWED_ROLES = [UserRoles.owner, AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_optional
    def get(self, pk):
        return super().get(pk)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
        ValidateSchema()
    )
    def put(self, pk):
        return super().put(pk)

    def get_schema_out(self, *args, **kwargs):
        # show not active shops only to admins and their owners
        current_user = auth.current_user()
        instance = kwargs.get('instance')

        if current_user \
                and current_user.role != UserRoles.customer \
                and (current_user.role in AdminRoles or current_user.id == instance.holder_id):
            return ShopExtendedSchemaOut

        return ShopShortSchemaOut if instance.active else NotFound("Shop not found!")


class ShopBrandPictureResource(DeleteImageResourceMixin):
    def delete(self, pk):
        pass
