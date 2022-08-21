from abc import ABC, abstractmethod

from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth_manager import auth
from models import AdminRoles
from utils.helpers import get_or_404


class BaseAccessValidator(ABC):
    ERROR_MESSAGE = ""
    CLASS_ERROR_MESSAGE_FIELD_NAME = ""

    def __init__(self, error_message=None):
        self.error_message = error_message

    @abstractmethod
    def validate(self, instance, *args, **kwargs):
        pass

    def _get_error_message(self, instance):
        """Return error message if it specified for the endpoint
        otherwise error message if it specified for the class
        and finally validator default error message"""
        return self.error_message or self._get_instance_error_message(instance) or self.ERROR_MESSAGE

    def _get_instance_error_message(self, instance):
        try:
            return getattr(instance, self.CLASS_ERROR_MESSAGE_FIELD_NAME)
        except AttributeError:
            return None


class ValidateRole(BaseAccessValidator):
    ERROR_MESSAGE = "Permission denied!"
    CLASS_ERROR_MESSAGE_FIELD_NAME = "PERMISSION_DENIED_MESSAGE"

    def __init__(self, allowed_roles=None, error_message=None):
        super().__init__(error_message)
        self.allowed_roles = allowed_roles

    def validate(self, instance, *args, **kwargs):
        allowed_roles = self.allowed_roles or instance.ALLOWED_ROLES
        current_user = auth.current_user()
        if not current_user:
            return
        if current_user.role not in allowed_roles:
            raise Forbidden(self._get_error_message(instance))


class ValidateIsOwner(BaseAccessValidator):
    ERROR_MESSAGE = "Permission denied!"
    CLASS_ERROR_MESSAGE_FIELD_NAME = "OWNER_REQUIRED_MESSAGE"

    def validate(self, instance, *args, **kwargs):
        current_user = auth.current_user()
        if current_user.role in AdminRoles:
            return

        pk = kwargs.get('pk')
        is_holder = instance.get_model().query.filter_by(id=pk).first().holder_id == current_user.id

        if not is_holder:
            raise Forbidden(self._get_error_message(instance))


class ValidatePageExist(BaseAccessValidator):
    ERROR_MESSAGE = "Page not found!"
    CLASS_ERROR_MESSAGE_FIELD_NAME = "NOT_FOUND_MESSAGE"

    def validate(self, instance, *args, **kwargs):
        get_or_404(instance.get_model(), kwargs.get("pk"), self._get_error_message(instance))


class ValidateUniqueness(BaseAccessValidator):
    ERROR_MESSAGE = "Unique constraint: Object already exist!"
    CLASS_ERROR_MESSAGE_FIELD_NAME = "UNIQUE_VALIDATION_MESSAGE"

    def validate(self, instance, *args, **kwargs):
        current_user = auth.current_user()
        if instance.get_model().query.filter_by(holder_id=current_user.id).first():
            raise Forbidden(self._get_error_message(instance))


class ValidateSchema:
    @staticmethod
    def validate(instance, *args, **kwargs):
        data = request.get_json()
        schema = instance.get_schema_in()
        errors = schema().validate(data)
        if errors:
            raise BadRequest(errors)
