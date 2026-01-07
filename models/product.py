# models/product.py
from datetime import datetime
from database import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=10)

    description = db.Column(db.Text)
    image_filename = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, default=True)   # for soft delete

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ----------------- RELATIONSHIPS -----------------

    # Seller who owns this product
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    seller = db.relationship(
        "User",
        back_populates="products",
        lazy=True
    )

    # Orders that contain this product
    orders = db.relationship(
        "Order",
        back_populates="product",
        lazy=True,
        cascade="all, delete-orphan"   # deleting product ⇒ delete its orders
    )

    def __repr__(self):
        return f"<Product {self.id} {self.name} (₹{self.price})>"
