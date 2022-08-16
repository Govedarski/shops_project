from flask import request
from flask_restful import Resource

from managers.user_manager import UserManager
from schemas.request.authentication_schemas_in import RegisterSchemaIn
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(RegisterSchemaIn)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201


class LoginResource(Resource):
    # @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {"token": token}, 200
