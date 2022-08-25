from marshmallow import Schema, validate, fields

from constants.extensions import VALID_PHOTO_EXTENSIONS, VALID_DOCUMENT_EXTENSIONS
from schemas.validators.common_validators import ValidateIsNumeric, ValidateIsAlphaAndSpace, \
    ValidateExtension


class ShopSchemaIn(Schema):
    name = fields.Str(required=True,
                      validate=validate.And(
                          validate.Length(min=2, max=64)))

    bulstat = fields.Str(required=True,
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

    website = fields.Url(validate=validate.Length(max=255))

    phone_number = fields.Str(
        validate=validate.And(
            validate.Length(equal=9),
            ValidateIsNumeric().validate
        ))

    description = fields.Str()

    brand_logo_photo = fields.String()

    brand_logo_extension = fields.String(validate=ValidateExtension("photos", VALID_PHOTO_EXTENSIONS).validate)

    verifying_documents_photo = fields.String(required=True)

    verifying_documents_extension = fields.String(required=True,
                                                  validate=ValidateExtension("documents",
                                                                             VALID_DOCUMENT_EXTENSIONS).validate)


class ShopChangeBrandLogoSchemaIn(Schema):
    brand_logo_photo = fields.String(required=True)

    brand_logo_extension = fields.String(required=True,
                                         validate=ValidateExtension("photos", VALID_PHOTO_EXTENSIONS).validate)
