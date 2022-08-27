from marshmallow import Schema, fields, validates_schema, ValidationError
from marshmallow_enum import EnumField

from models.enums import PaymentMethod


class OrderSchemaIn(Schema):
    products = fields.List(fields.Dict, required=True)

    payment_method = EnumField(PaymentMethod, required=True, error_messages={'by_name': "Invalid category"})

    @validates_schema
    def sanitize_data(self, data, **kwargs):
        for data in data['products']:
            if not isinstance(data.get('id'), int):
                raise ValidationError("Provided products data is invalid!")
            if not isinstance(data.get('quantity'), int) or data.get('quantity') < 0:
                raise ValidationError("Provided products data is invalid!")
