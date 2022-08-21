from datetime import datetime, timedelta

import jwt
from decouple import config
from flask import g, request
from flask_httpauth import HTTPTokenAuth
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized

from utils.helpers import get_user_or_admin_model


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(hours=2), "role": user.role.name}
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized("Missing token")
        try:
            payload = jwt.decode(token, key=config("JWT_SECRET"), algorithms=["HS256"])
            return {"id": payload["sub"], "role": payload["role"]}

        except ExpiredSignatureError:
            raise Unauthorized("Token expired")
        except InvalidTokenError:
            raise Unauthorized("Invalid token")


class Auth(HTTPTokenAuth):
    @staticmethod
    def login_optional(func):
        """Create current_user if there is request is authenticated"""

        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token:
                user_id, user_role = AuthManager.decode_token(token[7:]).values()
                model = get_user_or_admin_model(user_role)
                user = model.query.filter_by(id=user_id).first()
                g.flask_httpauth_user = user

            return func(*args, **kwargs)

        return wrapper


auth = Auth()


@auth.verify_token
def verify(token):
    user_id, user_role = AuthManager.decode_token(token).values()
    model = get_user_or_admin_model(user_role)
    return model.query.filter_by(id=user_id).first()
