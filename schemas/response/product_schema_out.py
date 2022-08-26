from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import ProductCategories


class ProductSchemaOut(Schema):
    id = fields.Integer(required=True)

    name = fields.Str(required=True)

    description = fields.Str()

    quantity = fields.Integer(required=True)

    price = fields.Float(required=True)

    category = EnumField(ProductCategories, required=True, by_name=True)

    in_shops = fields.List(fields.Integer)

    holder_id = fields.Integer()

    listed = fields.Boolean(required=True, default=False)
