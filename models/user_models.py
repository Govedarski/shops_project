from sqlalchemy import func
from sqlalchemy.orm import Query

from db import db
from models.enums import UserRoles, AdminRoles


class BaseUserModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)


class CustomerModel(BaseUserModel):
    __tablename__ = 'customer'
    query: Query

    role = db.Column(db.Enum(UserRoles), default=UserRoles.customer, nullable=False)
    # Todo link one-to-one to customer profile


class ShopOwnerModel(BaseUserModel):
    __tablename__ = 'shop_owner'
    query: Query

    role = db.Column(db.Enum(UserRoles), default=UserRoles.owner, nullable=False)
    # Todo link one-to-one to owner profile


class AdminModel(BaseUserModel):
    __tablename__ = 'admin'
    query: Query

    role = db.Column(db.Enum(AdminRoles), default=AdminRoles.admin, nullable=False)
