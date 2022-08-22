from managers.auth_manager import auth
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateUniqueness, ValidateSchema, \
    ValidatePageExist, ValidateIsHolder
from resources.helpers.crud_resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin, \
    DeleteImageResourceMixin
from utils.resource_decorators import execute_access_validators


class CreateDetailsResource(CreateResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateUniqueness(),
        ValidateSchema()
    )
    def post(self):
        return super().post()


class DetailsResource(GetResourceMixin, EditResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidatePageExist()
    )
    def get(self, pk):
        return super().get(pk)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
        ValidateSchema()
    )
    def put(self, pk):
        return super().put(pk)


class DetailsImageResource(DeleteImageResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateIsHolder(),
        ValidatePageExist(),
    )
    def delete(self, pk):
        return super().delete(pk)


class RemoveIbanSpacesMixin:
    def get_data(self):
        data = super().get_data()
        iban = data.get("iban")
        if iban:
            data["iban"] = data["iban"].replace(" ", "")

        return data
