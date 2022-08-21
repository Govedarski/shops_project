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
    def get_data():
        return request.get_json()

    def get_model(self):
        return self.MODEL

    def get_schema_in(self):
        return self.SCHEMA_IN

    def get_schema_out(self):
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
        return self.get_schema_out()().dump(instance), 200


class EditResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def put(self, pk):
        data = self.get_data()
        instance = CRUDManager.edit(self.get_model(), data, pk)
        return self.get_schema_out()().dump(instance), 200


class DeleteImageResourceMixin(ABC, BaseResource):
    """Minimum required class attributes: MODEL, IMAGE_FIELD_NAME, SCHEMA_OUT"""
    IMAGE_FIELD_NAME = ""

    @abstractmethod
    def delete(self, pk):
        instance = CRUDManager.delete_image(self.get_model(), pk, self.IMAGE_FIELD_NAME)
        return self.get_schema_out()().dump(instance), 200
