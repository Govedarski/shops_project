from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth_manager import AuthManager
from utils import helpers


class UserManager:
    @staticmethod
    def register(data):
        user_model = helpers.get_user_model(data.pop('role'))
        data["password"] = generate_password_hash(data["password"])
        user = user_model(**data)
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)

    @staticmethod
    def login(data):
        user_model = helpers.get_user_model(data.pop('role'))
        user = user_model.query.filter_by(email=data["identifier"]).first() \
               or user_model.query.filter_by(username=data["identifier"]).first()

        if user and check_password_hash(user.password, data["password"]):
            return AuthManager.encode_token(user)

        raise BadRequest("Wrong credentials!")
