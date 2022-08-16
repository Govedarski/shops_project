import factory

from db import db
from models import UserRoles, CustomerModel


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.commit()
        return object


class CustomerFactory(BaseFactory):
    class Meta:
        model = CustomerModel

    id = factory.Sequence(lambda n: n)
    username = factory.Faker('user_name')
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRoles.customer


class OwnerFactory(BaseFactory):
    class Meta:
        model = CustomerModel

    id = factory.Sequence(lambda n: n)
    username = factory.Faker('user_name')
    email = factory.Faker("email")
    password = factory.Faker("password")
    role = UserRoles.customer
