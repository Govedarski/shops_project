from flask import request
from flask_restful import Resource

from managers.user_manager import UserManager
from resources.access_endpoint_validators import ValidateSchema
from schemas.request.authentication_schemas_in import RegisterSchemaIn
from utils.resource_decorators import execute_access_validators


class RegisterResource(Resource):
    SCHEMA_IN = RegisterSchemaIn

    @execute_access_validators(ValidateSchema())
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}, 200
