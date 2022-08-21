from sqlalchemy import func
from sqlalchemy.orm import Query

from db import db
from models.mixins import ImageMixin


class BaseDetailsModel(db.Model, ImageMixin):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    phone_number = db.Column(db.String(9))
    age = db.Column(db.Integer)
    profile_picture_image_url = db.Column(db.String(255))

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    last_changed = db.Column(db.DateTime, onupdate=func.now())


class CustomerDetailsModel(BaseDetailsModel):
    __tablename__ = 'customer_details'
    __table_args__ = {'extend_existing': True}
    query: Query

    holder_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False, unique=True)


class ShopOwnerDetailsModel(BaseDetailsModel):
    __tablename__ = 'shop_owner_details'
    __table_args__ = {'extend_existing': True}
    query: Query
    iban = db.Column(db.String(22), nullable=False, unique=True)
    confirm_identity_documents_image_url = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    holder_id = db.Column(db.Integer, db.ForeignKey("shop_owner.id"), nullable=False, unique=True)


class DeliveryAddressDetailsModel(db.Model):
    __tablename__ = 'delivery_details'
    __table_args__ = {'extend_existing': True}
    query: Query

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    phone_number = db.Column(db.String(9), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text, nullable=False)

    extra_informations = db.Column(db.Text)

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    last_changed = db.Column(db.DateTime, onupdate=func.now())

    holder_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
