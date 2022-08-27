from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from marshmallow_enum import EnumField

from constants.extensions import VALID_PHOTO_EXTENSIONS
from models import ProductCategories
from schemas.validators.common_validators import ValidateExtension


class ProductSchemaIn(Schema):
    name = fields.Str(required=True,
                      validate=validate.And(
                          validate.Length(min=2, max=64),
                      ))

    description = fields.Str()

    quantity = fields.Integer(required=True,
                              validate=validate.Range(min=0))

    price = fields.Float(required=True,
                         validate=validate.Range(min=0))

    category = EnumField(ProductCategories, required=True, error_messages={'by_name': "Invalid category"})

    shops_id = fields.List(fields.Integer())

    listed = fields.Boolean(required=True, default=False)

    product_photo = fields.String()

    product_extension = fields.String(validate=ValidateExtension("photos", VALID_PHOTO_EXTENSIONS).validate)

    @validates_schema
    def sanitize_data(self, data, **kwargs):
        if data["listed"] and not data["shops_id"]:
            raise ValidationError("No shops provided")


class EditProductSchemaIn(ProductSchemaIn):
    name = fields.Str(required=True,
                      validate=validate.And(
                          validate.Length(min=2, max=64),
                      ))

    description = fields.Str()

    quantity = fields.Integer(required=True,
                              validate=validate.Range(min=0))

    price = fields.Float(required=True,
                         validate=validate.Range(min=0))

    category = EnumField(ProductCategories, required=True, error_messages={'by_name': "Invalid category"})

    shops_id = fields.List(fields.Integer())

    listed = fields.Boolean(required=True, default=False)

    @validates_schema
    def validate_shops(self, data, **kwargs):
        if data["listed"] and not data["shops_id"]:
            raise ValidationError("No shops provided!")
