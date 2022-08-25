from marshmallow import Schema, fields, validate

from constants.extensions import VALID_PHOTO_EXTENSIONS
from schemas.validators.common_validators import ValidateIsNumeric, ValidateExtension, ValidateIsAlpha


class DetailsSchemaIn(Schema):
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
    age = fields.Integer(validate=validate.Range(min=18, max=100))

    phone_number = fields.Str(validate=validate.And(
        validate.Length(equal=9),
        ValidateIsNumeric().validate
    ))

    profile_picture_photo = fields.String()

    profile_picture_extension = fields.String(validate=ValidateExtension("photos", VALID_PHOTO_EXTENSIONS).validate)


class ChangeProfilePictureSchemaIn(Schema):
    profile_picture_photo = fields.String(required=True)

    profile_picture_extension = fields.String(required=True,
                                              validate=ValidateExtension("photos", VALID_PHOTO_EXTENSIONS).validate)
