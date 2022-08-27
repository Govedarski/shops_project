from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models import ProductCategories
from schemas.response.shop_schemas_out import ShopShortSchemaOut


class ProductSchemaOut(Schema):
    id = fields.Integer(required=True)

    name = fields.Str(required=True)

    description = fields.Str()

    quantity = fields.Integer(required=True)

    price = fields.Float(required=True)

    category = EnumField(ProductCategories, required=True, by_name=True)

    in_shops = fields.List(fields.Nested(ShopShortSchemaOut))

    holder_id = fields.Integer()

    listed = fields.Boolean(required=True, default=False)
