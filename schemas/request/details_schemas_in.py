from marshmallow import Schema, fields, validate

from schemas.validators.common_validators import ValidateIsAlpha, ValidateIsNumeric, ValidatePhotoExtension


class BaseCustomerDetails(Schema):
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

    age = fields.Integer(validate=validate.Range(min=16, max=100))

    phone_number = fields.Str(validate=validate.And(
        validate.Length(equal=9),
        ValidateIsNumeric().validate
    ))


class CreateCustomerDetailsSchemaIn(BaseCustomerDetails):
    photo = fields.String()

    extension = fields.String(validate=ValidatePhotoExtension().validate)


class EditCustomerDetailsSchemaIn(BaseCustomerDetails):
    pass


class ChangeProfilePictureSchemaIn(Schema):
    photo = fields.String(required=True)

    extension = fields.String(required=True,
                              validate=ValidatePhotoExtension().validate)
