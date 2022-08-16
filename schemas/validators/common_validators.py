from marshmallow import ValidationError

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
            raise ValidationError(self._get_error_message(value))


class ValidateIsAlphaNumeric(BaseCustomValidator):
    ERROR = "Must contain only numbers and letters!"

    def validate(self, value):
        if not value.isalnum():
            raise ValidationError(self._get_error_message(value))
