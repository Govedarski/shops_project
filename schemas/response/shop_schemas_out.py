from marshmallow import Schema, fields


class ShopShortSchemaOut(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    city = fields.Str(required=True)
    website = fields.Str()
    description = fields.Str()
    brand_logo_image_url = fields.String()


class ShopExtendedSchemaOut(ShopShortSchemaOut):
    bulstat = fields.Str(required=True)
    address = fields.Str(required=True)
    phone_number = fields.Str()
    verifying_documents_image_url = fields.String(required=True)
    verified = fields.Boolean(required=True)
    active = fields.Boolean(required=True)
    holder_id = fields.Integer(required=True)
