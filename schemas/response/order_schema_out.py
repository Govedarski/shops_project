from marshmallow import Schema, fields


class OrderSchemaOut(Schema):
    id = fields.Integer(required=True)
