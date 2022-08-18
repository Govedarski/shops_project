from marshmallow import Schema, fields


class DetailsSchemaOut(Schema):
    first_name = fields.Str(required=True)

    last_name = fields.Str(required=True)

    age = fields.Integer()

    phone_number = fields.Str()

    profile_picture_url = fields.String()
