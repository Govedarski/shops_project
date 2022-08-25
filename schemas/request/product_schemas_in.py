from marshmallow import Schema, fields, validate, ValidationError, validates_schema, pre_load, post_load
from marshmallow_enum import EnumField

from managers.auth_manager import auth
from models import ProductCategories


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

    @validates_schema
    def validate_shops(self, data, **kwargs):
        if data["listed"] and not data["shops_id"]:
            raise ValidationError("No shops provided")

    @pre_load
    def pre_load(self, data, **kwargs):
        print(auth.current_user())

        print("PRE-Dump")
        print(data)
        return data

    @post_load
    def post_load(self, data, **kwargs):
        print(auth.current_user())
        data.pop("listed")
        print("POST-Dump")
        print(data)
        return data


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
            raise ValidationError("No shops provided")

# refactor the schemas_in
