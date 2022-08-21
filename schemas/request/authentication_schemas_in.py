from marshmallow import fields, Schema, validate
from marshmallow_enum import EnumField

from models import UserRoles, CustomerModel, ShopOwnerModel
from schemas.validators.common_validators import ValidateUniqueness, ValidateIsAlphaNumeric
from schemas.validators.password_validator import PasswordValidator


class RegisterSchemaIn(Schema):
    role = EnumField(UserRoles, required=True, error_messages={'by_name': "Invalid role"})

    email = fields.Email(required=True,
                         validate=validate.And(
                             ValidateUniqueness("email", CustomerModel, ShopOwnerModel).validate,
                         ))

    username = fields.Str(required=True,
                          validate=validate.And(
                              validate.Length(min=3, max=64),
                              ValidateIsAlphaNumeric().validate,
                              ValidateUniqueness("username", CustomerModel, ShopOwnerModel).validate,
                          ))

    password = fields.Str(required=True,
                          validate=PasswordValidator().validate_password)


class RegisterAdminSchemaIn(Schema):
    role = EnumField(UserRoles, required=True, error_messages={'by_name': "Invalid role"})
