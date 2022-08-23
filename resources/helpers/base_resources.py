from managers.auth_manager import auth
from models import AdminRoles
from resources.helpers.access_endpoint_validators import ValidateRole, ValidatePageExist, ValidateIsHolder
from resources.helpers.resources_mixins import EditResourceMixin, DeleteImageResourceMixin
from utils.resource_decorators import execute_access_validators


class VerifyBaseResource(EditResourceMixin):
    """Need MODEL AND SCHEMA_OUT"""
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidatePageExist(),
    )
    def put(self, pk):
        return super().put(pk)

    def get_data(self):
        return {"verified": True}


class RemoveImageBaseResource(DeleteImageResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def delete(self, pk):
        return super().delete(pk)
