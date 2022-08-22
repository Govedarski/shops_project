import factory

from db import db
from models import UserRoles, CustomerModel, AdminModel, AdminRoles, ShopOwnerModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class BaseUserFactory(BaseFactory):
    username = factory.Faker('user_name')
    email = factory.Faker("email")
    password = factory.Faker("password")


class CustomerFactory(BaseUserFactory):
    id = factory.Sequence(lambda n: n + 100)

    class Meta:
        model = CustomerModel

    role = UserRoles.customer


class OwnerFactory(BaseUserFactory):
    id = factory.Sequence(lambda n: n + 100)

    class Meta:
        model = ShopOwnerModel

    role = UserRoles.owner


class AdminFactory(BaseUserFactory):
    id = factory.Sequence(lambda n: n + 1000)

    class Meta:
        model = AdminModel

    role = AdminRoles.admin


class SuperAdminFactory(BaseUserFactory):
    id = factory.Sequence(lambda n: n + 10000)

    class Meta:
        model = AdminModel

    role = AdminRoles.super_admin
