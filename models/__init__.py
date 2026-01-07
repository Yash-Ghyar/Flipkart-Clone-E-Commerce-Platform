# models/__init__.py

from database import db

# Import models so they are registered with SQLAlchemy
from .user import User
from .product import Product
from .order import Order

__all__ = ["db", "User", "Product", "Order"]
