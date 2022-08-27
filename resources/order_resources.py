from managers.auth_manager import auth
from managers.order_manager import OrderManager
from models import UserRoles
from resources.helpers.resources_mixins import CreateResourceMixin
from schemas.request.order_schema_in import OrderSchemaIn
from schemas.response.order_schema_out import OrderSchemaOut


class OrderResource(CreateResourceMixin):
    MANAGER = OrderManager
    SCHEMA_IN = OrderSchemaIn
    SCHEMA_OUT = OrderSchemaOut
    ALLOWED_ROLES = [UserRoles.customer]

    @auth.login_optional
    def post(self):
        data = self.get_data()
        current_user = auth.current_user()
        instance, payment_link = self.get_manager()().create(
            data,
            current_user)
        return [
                   self.get_schema_out(instance=instance)(many=isinstance(instance, list)).dump(instance),
                   {"payment_link": payment_link}], 201
