from werkzeug.security import generate_password_hash

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

    # @staticmethod
    # def login(login_data):
    #     complainer = ComplainerModel.query.filter_by(email=login_data["email"]).first()
    #     if not complainer:
    #         raise BadRequest("No such email! Please register!")
    #
    #     if check_password_hash(complainer.password, login_data["password"]):
    #         return AuthManager.encode_token(complainer)
    #     raise BadRequest("Wrong credentials!")
