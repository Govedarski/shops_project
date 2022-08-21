from marshmallow import Schema, fields


class DetailsSchemaOut(Schema):
    id = fields.Integer(required=True)

    first_name = fields.Str(required=True)

    last_name = fields.Str(required=True)

    age = fields.Integer()

    phone_number = fields.Str()

    profile_picture_image_url = fields.String()


class ShopOwnerDetailsSchemaOut(DetailsSchemaOut):
    id = fields.Integer(required=True)

    iban = fields.String(required=True)

    confirm_identity_documents_image_url = fields.String(required=True)


class DeliveryAddressDetailsSchemaOut(Schema):
    id = fields.Integer(required=True)

    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone_number = fields.String(required=True)
    city = fields.String(required=True)
    address = fields.String(required=True)

    extra_informations = fields.String(required=True)

    holder_id = fields.Integer()
