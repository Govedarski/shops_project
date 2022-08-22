from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from db import db
from managers.auth_manager import AuthManager


class UserManager:
    UNIQUE_VALIDATION_MESSAGE = "Unique constraint violation!"
    CREDENTIALS_ERROR_MESSAGE = "Wrong credentials!"

    @classmethod
    def register(cls, user_model, data):
        if user_model.query.filter_by(username=data["username"]).first() or \
                user_model.query.filter_by(email=data["email"]).first():
            raise BadRequest(cls.UNIQUE_VALIDATION_MESSAGE)

        user = user_model(**data)
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)

    @classmethod
    def login(cls, user_model, data):
        user = user_model.query.filter_by(email=data["identifier"]).first() \
               or user_model.query.filter_by(username=data["identifier"]).first()

        if user and check_password_hash(user.password, data["password"]):
            return AuthManager.encode_token(user)

        raise BadRequest(cls.CREDENTIALS_ERROR_MESSAGE)
