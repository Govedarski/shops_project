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
    last_changed = db.Column(db.DateTime, onupdate=func.now())


class CustomerModel(BaseUserModel):
    __tablename__ = 'customer'
    __table_args__ = {'extend_existing': True}
    query: Query

    role = db.Column(db.Enum(UserRoles), default=UserRoles.customer, nullable=False)

    details = db.relationship('CustomerDetailsModel', backref='customer', uselist=False)
    delivery_address = db.relationship('DeliveryAddressDetailsModel', backref='customer')


class ShopOwnerModel(BaseUserModel):
    __tablename__ = 'shop_owner'
    __table_args__ = {'extend_existing': True}
    query: Query

    role = db.Column(db.Enum(UserRoles), default=UserRoles.owner, nullable=False)
    details = db.relationship('ShopOwnerDetailsModel', backref='shop_owner', uselist=False)
    shops = db.relationship('ShopModel', backref='shop_owner')


class AdminModel(BaseUserModel):
    __tablename__ = 'admin'
    query: Query

    role = db.Column(db.Enum(AdminRoles), default=AdminRoles.admin, nullable=False)
