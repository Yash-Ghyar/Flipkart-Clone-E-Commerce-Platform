# routes/__init__.py

from .users import users_bp
from .products import products_bp
from .orders import orders_bp
from .admin import admin_bp

__all__ = ["users_bp", "products_bp", "orders_bp", "admin_bp"]
