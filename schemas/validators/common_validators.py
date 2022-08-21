from marshmallow import ValidationError
from schwifty import IBAN

from schemas.validators.base_custom_validator import BaseCustomValidator


class ValidateUniqueness(BaseCustomValidator):
    ERROR = "is already taken"

    def __init__(self, column, *models):
        self.models = models
        self.column = column

    def validate(self, value):
        criteria = {self.column: value}
        for model in self.models:
            obj = model.query.filter_by(**criteria).first()
            if obj:
                raise ValidationError(self._get_error_message(value))

    def _get_error_message(self, value):
        return value + ' ' + self.ERROR


class ValidateIsAlpha(BaseCustomValidator):
    ERROR = "Must contain only letters!"

    def validate(self, value):
        if not value.isalpha():
            raise ValidationError(self.ERROR)


class ValidateIsAlphaAndSpace(BaseCustomValidator):
    ERROR = "Must contain only letters and spaces!"

    def validate(self, value):
        if not value.replace(" ", "").isalpha():
            raise ValidationError(self.ERROR)


class ValidateIsAlphaNumeric(BaseCustomValidator):
    ERROR = "Must contain only numbers and letters!"

    def validate(self, value):
        if not value.isalnum():
            raise ValidationError(self.ERROR)


class ValidateIsNumeric(BaseCustomValidator):
    ERROR = "Must contain only numbers!"

    def validate(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(self.ERROR)


class ValidateIBAN(BaseCustomValidator):
    ERROR = "Invalid iban!"

    def validate(self, value):
        try:
            IBAN(value, validate_bban=True)
        except ValueError:
            raise ValidationError(self.ERROR)


class ValidateExtension:
    def __init__(self, file_type, valid_extensions):
        self.file_type = file_type
        self.valid_extensions = valid_extensions

    def validate(self, value):
        if value not in self.valid_extensions:
            raise ValidationError(f"Valid extension for {self.file_type} are {', '.join(self.valid_extensions)}!")
