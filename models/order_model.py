from sqlalchemy.orm import Query

from db import db
from models.enums import PaymentMethod


class OrderProductModel(db.Model):
    __tablename__ = "order_products"
    order_id = db.Column("order_id", db.ForeignKey("order.id"), primary_key=True)
    product_id = db.Column("product_id", db.ForeignKey("product.id"), primary_key=True)
    order_quantity = db.Column(db.Integer, nullable=False, default=0)
    order_price = db.Column(db.Float, nullable=False, default=0)

    product = db.relationship("ProductModel", backref="order")


class OrderModel(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}

    query: Query

    id = db.Column(db.Integer, primary_key=True)

    products = db.relationship("OrderProductModel")

    payment_method = db.Column(db.Enum(PaymentMethod), nullable=False)

    payed = db.Column(db.Boolean, nullable=False, default=False)

    sent = db.Column(db.Boolean, nullable=False, default=False)

    total_price = db.Column(db.Float, nullable=False, default=0.0)
