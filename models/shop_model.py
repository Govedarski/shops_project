from sqlalchemy import func
from sqlalchemy.orm import Query

from db import db


class ShopModel(db.Model):
    __tablename__ = 'shop'
    query: Query

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False, unique=True)
    bulstat = db.Column(db.String(9))

    city = db.Column(db.String(64), nullable=False)
    address = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(255))
    phone_number = db.Column(db.String(9))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    confirm_documents = db.Column(db.String(255), nullable=False)
    confirm = db.Column(db.Boolean, nullable=False, default=False)

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    last_changed = db.Column(db.DateTime, onupdate=func.now())

    shop_owner_id = db.Column(db.Integer, db.ForeignKey("shop_owner.id"), nullable=False)


class CategoryModel(db.Model):
    __tablename__ = 'category'
    query: Query

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    shops = db.relationship("ShopModel", backref="category")
