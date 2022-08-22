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

    @staticmethod
    def get_data(*args, **kwargs):
        return request.get_json() if request.data else None

    def get_model(self, *args, **kwargs):
        return self.MODEL

    def get_schema_in(self, *args, **kwargs):
        return self.SCHEMA_IN

    def get_schema_out(self, *args, **kwargs):
        return self.SCHEMA_OUT


class CreateResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def post(self):
        data = self.get_data()
        current_user = auth.current_user()
        instance = CRUDManager.create(self.get_model(), data, current_user)
        return self.get_schema_out()().dump(instance), 201


class GetResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def get(self, pk):
        instance = CRUDManager.get(self.get_model(), pk)
        return self.get_schema_out(pk=pk)().dump(instance), 200


class GetListResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def get(self):
        obj_list = CRUDManager.get_all(self.get_model(), self.filter_by())
        return [self.get_schema_out()().dump(instance) for instance in obj_list if instance], 200

    def filter_by(self):
        return None


class EditResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def put(self, pk):
        data = self.get_data()
        instance = CRUDManager.edit(self.get_model(), data, pk)
        return self.get_schema_out(pk=pk)().dump(instance), 200


class DeleteResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL"""

    @abstractmethod
    def delete(self, pk):
        CRUDManager.delete(self.get_model(), pk)
        return None, 204


class DeleteImageResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, IMAGE_FIELD_NAME, SCHEMA_OUT"""
    IMAGE_FIELD_NAME = ""

    @abstractmethod
    def delete(self, pk):
        instance = CRUDManager.delete_image(self.get_model(), pk, self.IMAGE_FIELD_NAME)
        return self.get_schema_out()().dump(instance), 200
