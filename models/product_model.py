from sqlalchemy import func
from sqlalchemy.orm import Query

from db import db
from models.enums import ProductCategories
from models.mixins import ImageMixin


class ProductModel(db.Model, ImageMixin):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}

    query: Query

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), nullable=False)

    product_image_url = db.Column(db.String(255))

    description = db.Column(db.Text)

    quantity = db.Column(db.Integer, nullable=False, default=0)

    price = db.Column(db.Float, nullable=False, default=0)

    category = db.Column(db.Enum(ProductCategories), nullable=False)

    registered_on = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    last_changed = db.Column(db.DateTime, onupdate=func.now())

    holder_id = db.Column(db.Integer, db.ForeignKey("shop_owner.id"), nullable=False)

    listed = db.Column(db.Boolean, nullable=False, default=False)

    stripe_price_id = db.Column(db.String(255), unique=True)

    stripe_product_id = db.Column(db.String(255), unique=True)
