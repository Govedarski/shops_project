from sqlalchemy import func
from sqlalchemy.orm import Query

from db import db


class BaseDetailsModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    phone_number = db.Column(db.String(9))
    age = db.Column(db.Integer)
    profile_picture_url = db.Column(db.String(255))

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    last_changed = db.Column(db.DateTime, onupdate=func.now())


class CustomerDetailsModel(BaseDetailsModel):
    __tablename__ = 'customer_details'
    query: Query

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False, unique=True)


class ShopOwnerDetailsModel(BaseDetailsModel):
    __tablename__ = 'shop_owner_details'
    query: Query
    iban = db.Column(db.String(22), nullable=False, unique=True)
    confirm_identity_documents = db.Column(db.String(255), nullable=False)
    confirm = db.Column(db.Boolean, nullable=False, default=False)

    shop_owner_id = db.Column(db.Integer, db.ForeignKey("shop_owner.id"), nullable=False)


class DeliveryAddressDetailsModel(db.Model):
    __tablename__ = 'delivery_details'
    query: Query

    id = db.Column(db.Integer, primary_key=True)

    city = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text, nullable=False)
    extra_informations = db.Column(db.Text)

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    last_changed = db.Column(db.DateTime, onupdate=func.now())

    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
