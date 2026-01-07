# app.py

from flask import Flask, render_template
from config import Config

from models import db
from models.product import Product

from routes.users import users_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.admin import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Init DB ---
    db.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(users_bp)          # /login, /register, /dashboard, etc.
    app.register_blueprint(products_bp)       # /products, /product/<id>, seller product CRUD
    app.register_blueprint(orders_bp)         # /orders/...
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ---------------------------
    # HOME PAGE  (Trending products)
    # ---------------------------
    @app.route("/")
    def home():
        trending_products = (
            Product.query
            .filter_by(is_active=True)
            .order_by(Product.created_at.desc())
            .limit(8)
            .all()
        )

        return render_template(
            "home.html",
            trending_products=trending_products,
        )

    # ---------------------------
    # ERROR HANDLERS
    # ---------------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html", message="Page not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("error.html", message="Something went wrong"), 500

    return app


# Global app instance so create_db.py can do: from app import app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
