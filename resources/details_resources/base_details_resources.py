from managers.auth_manager import auth
from resources.helpers.access_endpoint_validators import ValidateRole, ValidateSchema
from resources.helpers.resources_mixins import CreateResourceMixin, GetResourceMixin, EditResourceMixin
from utils.resource_decorators import execute_access_validators


class CreateDetailsResource(CreateResourceMixin):
    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema()
    )
    def post(self):
        return super().post()


class DetailsResource(GetResourceMixin, EditResourceMixin):
    @auth.login_required
    def get(self, pk, *args, **kwargs):
        return super().get(pk, *args, **kwargs)

    @auth.login_required
    @execute_access_validators(
        ValidateRole(),
        ValidateSchema()
    )
    def put(self, pk):
        current_user = auth.current_user()

        return super().put(pk, user=current_user, holder_required=True)


class RemoveIbanSpacesMixin:
    def get_data(self):
        data = super().get_data()
        iban = data.get("iban")
        if iban:
            data["iban"] = data["iban"].replace(" ", "")

        return data
