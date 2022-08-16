from flask import request
from flask_restful import Resource

from managers.user_manager import UserManager


class RegisterResource(Resource):
    # @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {"token": token}, 201

# class LoginResource(Resource):
#     @validate_schema(LoginSchemaRequest)
#     def post(self):
#         data = request.get_json()
#         token = ComplainerManager.login(data)
#         return {"token": token}, status.HTTP_200_OK
#
#
# class ApproverLoginResource(Resource):
#     @validate_schema(LoginSchemaRequest)
#     def post(self):
#         data = request.get_json()
#         token = ApproverManager.login(data)
#         return {"token": token},  status.HTTP_200_OK
