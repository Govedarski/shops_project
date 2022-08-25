from managers.auth_manager import auth
from managers.user_manager import UserManager
from models import AdminRoles
from resources.helpers.access_validators import ValidateSchema, ValidateRole
from resources.helpers.resources_mixins import BaseResource
from schemas.request.authentication_schemas_in import RegisterSchemaIn, RegisterAdminSchemaIn, LoginSchemaIn
from utils.decorators import execute_access_validators


class RegisterResource(BaseResource):
    SCHEMA_IN = RegisterSchemaIn

    @execute_access_validators(ValidateSchema())
    def post(self):
        data = self.get_data()
        token = UserManager.register(data)
        return {"token": token}, 201


class RegisterAdminResource(BaseResource):
    SCHEMA_IN = RegisterAdminSchemaIn
    ALLOWED_ROLES = [AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema()
    )
    def post(self):
        data = self.get_data()
        result = UserManager.register_admin(data)
        return result, 200


class LoginResource(BaseResource):
    SCHEMA_IN = LoginSchemaIn

    def post(self):
        data = self.get_data()
        token = UserManager.login(data)
        return {"token": token}, 200
