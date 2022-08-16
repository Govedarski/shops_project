from marshmallow import fields, Schema
from marshmallow_enum import EnumField

from models import UserRoles


class RegisterSchemaIn(Schema):
    email = fields.Email(required=True)

    username = fields.Str(required=True)

    password = fields.Str(required=True)

    role = EnumField(UserRoles, required=True, error_messages={'by_name': "Invalid role"})
