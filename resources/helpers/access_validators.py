from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth_manager import auth
from models import AdminRoles


class ValidateRole:
    ERROR_MESSAGE = "Permission denied!"

    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles

    def validate(self, instance, *args, **kwargs):
        allowed_roles = self.allowed_roles or instance.ALLOWED_ROLES
        current_user = auth.current_user()
        if not current_user:
            return
        if current_user.role == AdminRoles.super_admin:
            return
        if current_user.role not in allowed_roles:
            raise Forbidden(self.ERROR_MESSAGE)


class ValidateSchema:
    def __init__(self, schema=None, many=False):
        self.schema = schema
        self.many = many

    def validate(self, instance, *args, **kwargs):
        data = request.get_json()
        schema = self.schema or instance.get_schema_in(*args, **kwargs)
        errors = schema(many=self.many).validate(data)

        if errors:
            raise BadRequest(errors)
