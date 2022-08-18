from flask import request
from flask_restful import Resource

from managers.auth_manager import auth
from managers.details_managers import CustomerDetailsManager
from models import UserRoles
from schemas.request.details_schemas_in import ChangeProfilePictureSchemaIn, CreateCustomerDetailsSchemaIn, \
    EditCustomerDetailsSchemaIn
from schemas.response.details_schemas_out import DetailsSchemaOut
from utils.decorators import permission_required, validate_schema


class CreateCustomerDetailsResource(Resource):
    @auth.login_required
    @permission_required(UserRoles.customer)
    @validate_schema(CreateCustomerDetailsSchemaIn)
    def post(self):
        data = request.get_json()
        current_user = auth.current_user()
        customer_details = CustomerDetailsManager.create(data, current_user)
        return DetailsSchemaOut().dump(customer_details), 201


class CustomerDetailsResource(Resource):
    @auth.login_required
    def get(self, pk):
        customer_details = CustomerDetailsManager.get_details(pk)
        return DetailsSchemaOut().dump(customer_details), 200

    @auth.login_required
    @permission_required(UserRoles.customer)
    @validate_schema(EditCustomerDetailsSchemaIn)
    def put(self, pk):
        data = request.get_json()
        customer_details = CustomerDetailsManager.edit(data, pk)
        return DetailsSchemaOut().dump(customer_details), 200


class ProfilePictureResource(Resource):
    @auth.login_required
    @permission_required(UserRoles.customer)
    @validate_schema(ChangeProfilePictureSchemaIn)
    def put(self, pk):
        data = request.get_json()
        customer_details = CustomerDetailsManager.change_profile_picture(data, pk)
        return DetailsSchemaOut().dump(customer_details), 200

    @auth.login_required
    @permission_required(UserRoles.customer)
    def delete(self, pk):
        customer_details = CustomerDetailsManager.delete_profile_picture(pk)
        return DetailsSchemaOut().dump(customer_details), 200
