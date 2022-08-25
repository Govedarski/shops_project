from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash

from db import db
from managers.auth_manager import AuthManager
from models import AdminRoles
from utils import helpers
from utils.decorators import handle_unique_constrain_violation


class UserManager:
    ADMIN_UNIQUE_VALIDATION_MESSAGE = "This user is already admin!"
    CREDENTIALS_ERROR_MESSAGE = "Wrong credentials!"

    @classmethod
    @handle_unique_constrain_violation
    def register(cls, data):
        user_model = cls._get_model(data.pop("role").name)

        user = user_model(**data)
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)

    @classmethod
    def register_admin(cls, data):
        user_model = cls._get_model(data['role'].name)
        user = user_model.query.filter_by(id=data["id"]).first()

        admin_data = cls._get_admin_data(user)
        admin_model = cls._get_model(admin_data['role'].name)

        if admin_model.query.filter_by(username=admin_data["username"]).first() or \
                admin_model.query.filter_by(email=admin_data["email"]).first():
            raise BadRequest(cls.ADMIN_UNIQUE_VALIDATION_MESSAGE)

        admin = admin_model(**admin_data)
        db.session.add(admin)
        db.session.flush()
        return {"updated": True}

    @classmethod
    def login(cls, data):
        user_model = cls._get_model(data.pop("role"))

        user = user_model.query.filter_by(email=data["identifier"]).first() \
               or user_model.query.filter_by(username=data["identifier"]).first()

        if user and check_password_hash(user.password, data["password"]):
            return AuthManager.encode_token(user)

        raise BadRequest(cls.CREDENTIALS_ERROR_MESSAGE)

    @staticmethod
    def _get_model(role):
        return helpers.get_user_or_admin_model(role)

    @staticmethod
    def _get_admin_data(user):
        return {
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "role": AdminRoles.admin
        }
