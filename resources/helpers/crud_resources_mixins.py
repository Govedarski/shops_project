from abc import ABC, abstractmethod

from flask import request
from flask_restful import Resource

from managers.auth_manager import auth
from managers.crud_manager import CRUDManager


class BaseResource(Resource):
    # Extended Resource class
    MODEL = None
    SCHEMA_IN = None
    SCHEMA_OUT = None
    MANAGER = CRUDManager

    @staticmethod
    def get_data(*args, **kwargs):
        return request.get_json() if request.data else None

    def get_model(self, *args, **kwargs):
        return self.MODEL

    def get_schema_in(self, *args, **kwargs):
        return self.SCHEMA_IN

    def get_schema_out(self, *args, **kwargs):
        return self.SCHEMA_OUT

    def get_manager(self, *args, **kwargs):
        return self.MANAGER


class CreateResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def post(self, **kwargs):
        data = self.get_data()
        current_user = auth.current_user()
        instance = self.get_manager().create(self.get_model(), data, current_user, **kwargs)
        return self.get_schema_out(instance=instance)().dump(instance), 201


class GetResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def get(self, pk, **kwargs):
        instance = self.get_manager().get(self.get_model(), pk, **kwargs)
        return self.get_schema_out(instance=instance)().dump(instance), 200


class GetListResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def get(self, **kwargs):
        obj_list = self.get_manager().get_list(self.get_model(), self.filter_by(), **kwargs)
        return [self.get_schema_out(instance=instance)().dump(instance) for instance in obj_list if instance], 200

    def filter_by(self):
        return None


class EditResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def put(self, pk, **kwargs):
        data = self.get_data()
        instance = self.get_manager().edit(self.get_model(), data, pk, **kwargs)
        return self.get_schema_out(instance=instance)().dump(instance), 200


class DeleteResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL"""

    @abstractmethod
    def delete(self, pk, **kwargs):
        self.get_manager().delete(self.get_model(), pk, **kwargs)
        return None, 204


class DeleteImageResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, IMAGE_FIELD_NAME, SCHEMA_OUT"""
    IMAGE_FIELD_NAME = ""

    @abstractmethod
    def delete(self, pk, **kwargs):
        instance = self.get_manager().delete_image(self.get_model(), pk, self.IMAGE_FIELD_NAME, **kwargs)
        return self.get_schema_out(instace=instance)().dump(instance), 200
