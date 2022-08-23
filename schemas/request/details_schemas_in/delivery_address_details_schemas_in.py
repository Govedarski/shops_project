from marshmallow import fields, validate, Schema

from schemas.validators.common_validators import ValidateIsAlpha, ValidateIsNumeric, ValidateIsAlphaAndSpace


class AuthCreateDeliveryAddressDetailsSchemaIn(Schema):
    phone_number = fields.Str(required=True,
                              validate=validate.And(
                                  validate.Length(equal=9),
                                  ValidateIsNumeric().validate
                              ))

    city = fields.Str(required=True,
                      validate=validate.And(
                          validate.Length(min=2, max=64),
                          ValidateIsAlphaAndSpace().validate
                      ))

    address = fields.Str(required=True)

    extra_informations = fields.Str()


class NoAuthCreateDeliveryAddressDetailsSchemaIn(AuthCreateDeliveryAddressDetailsSchemaIn):
    first_name = fields.Str(required=True,
                            validate=validate.And(
                                validate.Length(min=2, max=64),
                                ValidateIsAlpha().validate
                            ))

    last_name = fields.Str(required=True,
                           validate=validate.And(
                               validate.Length(min=2, max=64),
                               ValidateIsAlpha().validate
                           ))


class EditDeliveryAddressDetailsSchemaIn(Schema):
    phone_number = fields.Str(
        validate=validate.And(
            validate.Length(equal=9),
            ValidateIsNumeric().validate
        ))

    city = fields.Str(
        validate=validate.And(
            validate.Length(min=2, max=64),
            ValidateIsAlphaAndSpace().validate
        ))

    address = fields.Str()

    extra_informations = fields.Str()
