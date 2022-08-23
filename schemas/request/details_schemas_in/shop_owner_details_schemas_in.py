from marshmallow import fields

from constants.extensions import VALID_DOCUMENT_EXTENSIONS
from schemas.request.details_schemas_in.base_details_schemas_in import CreateDetailsSchemaIn, EditDetailsSchemaIn
from schemas.validators.common_validators import ValidateExtension, ValidateIBAN


class CreateShopOwnerDetailsSchemaIn(CreateDetailsSchemaIn):
    iban = fields.String(required=True, validate=ValidateIBAN().validate)

    confirm_identity_documents_photo = fields.String(required=True)
    confirm_identity_documents_extension = fields.String(required=True,
                                                         validate=ValidateExtension("documents",
                                                                                    VALID_DOCUMENT_EXTENSIONS).validate)


class EditShopOwnerDetailsSchemaIn(EditDetailsSchemaIn):
    iban = fields.String(validate=ValidateIBAN().validate)
