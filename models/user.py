# models/user.py
from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # store only hashed password
    password_hash = db.Column(db.String(255), nullable=False)

    # 'customer' | 'seller' | 'admin'
    role = db.Column(db.String(20), default="customer", nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---------- PASSWORD HELPERS ----------
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # ---------- RELATIONSHIPS ----------
    products = db.relationship("Product", back_populates="seller", lazy=True)
    orders = db.relationship("Order", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.id} {self.email} ({self.role})>"
