from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth_manager import auth


def validate_schema(schema_name):
    def decorated_functions(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if errors:
                raise BadRequest(errors)

            return func(*args, **kwargs)

        return wrapper

    return decorated_functions


def permission_required(*allowed_roles):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role not in allowed_roles:
                raise Forbidden("Permission denied!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function
