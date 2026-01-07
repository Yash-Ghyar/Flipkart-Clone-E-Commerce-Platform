# models/order.py
from datetime import datetime
from database import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    # FK to product & buyer user
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    quantity = db.Column(db.Integer, default=1, nullable=False)

    # Shipping / order status
    # Examples: "Pending", "Shipped", "Delivered", "Cancelled"
    status = db.Column(db.String(20), default="Pending", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # --------------- RELATIONSHIPS ----------------

    # Product in this order
    product = db.relationship(
        "Product",
        back_populates="orders",
        lazy=True
    )

    # Customer who placed this order
    user = db.relationship(
        "User",
        back_populates="orders",
        lazy=True
    )

    def __repr__(self):
        return f"<Order {self.id} user={self.user_id} product={self.product_id} qty={self.quantity}>"
