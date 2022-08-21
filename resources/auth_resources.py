from werkzeug.security import generate_password_hash

from managers.auth_manager import auth
from managers.user_manager import UserManager
from models import AdminRoles, AdminModel
from resources.helpers.access_endpoint_validators import ValidateSchema, ValidateRole, ValidatePageExist
from resources.helpers.crud_resources_mixins import BaseResource
from schemas.request.authentication_schemas_in import RegisterSchemaIn, RegisterAdminSchemaIn
from utils import helpers
from utils.resource_decorators import execute_access_validators


class RegisterResource(BaseResource):
    SCHEMA_IN = RegisterSchemaIn

    @execute_access_validators(ValidateSchema())
    def post(self):
        user_model = self.get_model()
        data = self.get_data()
        data.pop('role')
        token = UserManager.register(user_model, data)
        return {"token": token}, 201

    def get_data(self):
        data = super().get_data()
        data["password"] = generate_password_hash(data["password"])
        return data

    def get_model(self):
        return helpers.get_user_model(self.get_data()['role'])


class RegisterAdminResource(BaseResource):
    SCHEMA_IN = RegisterAdminSchemaIn
    ALLOWED_ROLES = [AdminRoles.super_admin]

    @auth.login_required
    @execute_access_validators(
        ValidatePageExist(),
        ValidateRole(),
        ValidateSchema()
    )
    def post(self, pk):
        user_model = self.get_model()
        user = user_model.query.filter_by(id=pk).first()
        data = self._get_admin_data(user)
        UserManager.register(AdminModel, data)
        return {}, 204

    def get_model(self):
        return helpers.get_user_model(self.get_data()['role'])

    @staticmethod
    def _get_admin_data(user):
        return {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "role": AdminRoles.admin
        }


class LoginResource(BaseResource):
    def post(self):
        user_model = self.get_model()
        data = self.get_data()
        data.pop('role')
        token = UserManager.login(user_model, data)
        return {"token": token}, 200

    def get_data(self):
        data = super().get_data()
        return data

    def get_model(self):
        return helpers.get_user_or_admin_model(self.get_data()['role'])
