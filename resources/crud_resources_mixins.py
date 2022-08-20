from abc import ABC, abstractmethod

from flask import request
from flask_restful import Resource

from managers.auth_manager import auth
from managers.crud_manager import CRUDManager


class BaseResourceMixin(Resource):
    MODEL = None
    SCHEMA_OUT = None

    @staticmethod
    def get_data():
        return request.get_json()


class CreateResourceMixin(ABC, BaseResourceMixin):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def post(self):
        data = self.get_data()
        current_user = auth.current_user()
        instance = CRUDManager.create(data, current_user, self.MODEL)
        return self.SCHEMA_OUT().dump(instance), 201


class GetResourceMixin(ABC, BaseResourceMixin):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def get(self, pk):
        instance = CRUDManager.get(pk, self.MODEL)
        return self.SCHEMA_OUT().dump(instance), 200


class EditResourceMixin(ABC, BaseResourceMixin):
    """Minimum required class attributes: MODEL, SCHEMA_OUT"""

    @abstractmethod
    def put(self, pk):
        data = self.get_data()
        instance = CRUDManager.edit(data, pk, self.MODEL)
        return self.SCHEMA_OUT().dump(instance), 200


class DeleteImageResourceMixin(ABC, BaseResourceMixin):
    """Minimum required class attributes: MODEL, IMAGE_FIELD_NAME, SCHEMA_OUT"""
    IMAGE_FIELD_NAME = ""

    @abstractmethod
    def delete(self, pk):
        instance = CRUDManager.delete_image(pk, self.MODEL, self.IMAGE_FIELD_NAME)
        return self.SCHEMA_OUT().dump(instance), 200
