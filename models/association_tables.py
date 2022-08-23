from db import db

shops_products = db.Table(
    "shops_products",
    db.Model.metadata,
    db.Column("shop_id", db.Integer, db.ForeignKey("shop.id")),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id")),
)
