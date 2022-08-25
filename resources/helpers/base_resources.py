from managers.auth_manager import auth
from models import AdminRoles
from resources.helpers.access_validators import ValidateRole
from resources.helpers.resources_mixins import EditResourceMixin, DeleteImageResourceMixin
from utils.decorators import execute_access_validators


class VerifyBaseResource(EditResourceMixin):
    """Need MODEL AND SCHEMA_OUT"""
    ALLOWED_ROLES = [AdminRoles.admin, AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def put(self, pk):
        return super().put(pk)

    def get_data(self):
        return {"verified": True}


class RemoveImageBaseResource(DeleteImageResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
    )
    def delete(self, pk, **kwargs):
        return super().delete(
            pk,
            holder_required=True,
            user=auth.current_user(),
            **kwargs)
