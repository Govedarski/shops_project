from marshmallow import fields

from constants.extensions import VALID_DOCUMENT_EXTENSIONS
from schemas.request.details_schemas_in.base_details_schemas_in import DetailsSchemaIn
from schemas.validators.common_validators import ValidateExtension, ValidateIBAN


class ShopOwnerDetailsSchemaIn(DetailsSchemaIn):
    iban = fields.String(required=True, validate=ValidateIBAN().validate)

    confirm_identity_documents_photo = fields.String(required=True)
    confirm_identity_documents_extension = fields.String(required=True,
                                                         validate=ValidateExtension("documents",
                                                                                    VALID_DOCUMENT_EXTENSIONS).validate)
