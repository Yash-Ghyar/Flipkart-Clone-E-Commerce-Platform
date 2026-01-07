# routes/users.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

from models import db
from models.user import User
from models.product import Product
from models.order import Order

from utils.decorators import login_required
from validators import is_valid_email, is_strong_password

users_bp = Blueprint("users", __name__)


# -----------------------------------------------------------
# CUSTOMER + SELLER REGISTRATION  (/register)
# -----------------------------------------------------------
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()
        role = (request.form.get("role") or "customer").lower()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
            return render_template("auth/register.html")

        if not is_strong_password(password):
            flash("Password must be at least 6 characters.", "danger")
            return render_template("auth/register.html")

        # no direct admin signup here
        if role not in ["customer", "seller"]:
            role = "customer"

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("users.login"))

        user = User(
            name=name,
            email=email,
            role=role,
            created_at=datetime.utcnow()
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("users.login"))

    return render_template("auth/register.html")


# -----------------------------------------------------------
# SELLER REGISTER SEPARATE PAGE  (/seller/register)
# -----------------------------------------------------------
@users_bp.route("/seller/register", methods=["GET", "POST"])
def seller_register():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/seller_register.html")

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for("users.seller_register"))

        seller = User(
            name=name,
            email=email,
            role="seller",
            created_at=datetime.utcnow()
        )
        seller.set_password(password)

        db.session.add(seller)
        db.session.commit()

        flash("Seller account created successfully! Please login.", "success")
        return redirect(url_for("users.login"))

    return render_template("auth/seller_register.html")


# -----------------------------------------------------------
# LOGIN  (/login)
# -----------------------------------------------------------
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("users.login"))

        # store session
        session["logged_in"] = True
        session["user_id"] = user.id
        session["role"] = user.role

        flash("Login successful!", "success")
        return redirect(url_for("users.dashboard"))

    return render_template("auth/login.html")


# -----------------------------------------------------------
# LOGOUT  (/logout)
# -----------------------------------------------------------
@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


# -----------------------------------------------------------
# SUPER SECRET ADMIN REGISTER (LOCALHOST ONLY)
# URL: /super-secret-admin-register-982174
# FORM: only EMAIL + PASSWORD needed
# -----------------------------------------------------------
@users_bp.route("/super-secret-admin-register-982174", methods=["GET", "POST"])
def secret_admin_register():
    # Only allow from your own machine
    if request.remote_addr not in ["127.0.0.1", "::1"]:
        return "Access Denied", 403

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = (request.form.get("password") or "").strip()

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("auth/admin_register.html")

        if not is_valid_email(email):
            flash("Invalid email format.", "danger")
            return render_template("auth/admin_register.html")

        if not is_strong_password(password):
            flash("Password must be at least 6 characters.", "danger")
            return render_template("auth/admin_register.html")

        if User.query.filter_by(email=email).first():
            flash("Admin with this email already exists.", "danger")
            return render_template("auth/admin_register.html")

        # if no name field in form, derive name from email
        name = email.split("@")[0] or "Admin"

        admin = User(
            name=name,
            email=email,
            role="admin",
            created_at=datetime.utcnow()
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        flash("Admin created successfully! Please login.", "success")
        return redirect(url_for("users.login"))

    return render_template("auth/admin_register.html")


# -----------------------------------------------------------
# ROLE-BASED DASHBOARD  (/dashboard)
# -----------------------------------------------------------
@users_bp.route("/dashboard")
@login_required
def dashboard():
    role = session.get("role")
    user_id = session.get("user_id")

    # ADMIN DASHBOARD
    if role == "admin":
        user_count = User.query.count()
        product_count = Product.query.count()
        order_count = Order.query.count()

        return render_template(
            "dashboards/admin_dashboard.html",
            user_count=user_count,
            product_count=product_count,
            order_count=order_count,
        )

    # SELLER DASHBOARD
    if role == "seller":
        products = Product.query.filter_by(seller_id=user_id).all()

        orders = (
            Order.query
            .join(Product)
            .filter(Product.seller_id == user_id)
            .all()
        )

        total_revenue = sum(
            o.product.price * o.quantity
            for o in orders
            if o.product
        )

        return render_template(
            "dashboards/seller_dashboard.html",
            products=products,
            product_count=len(products),
            order_count=len(orders),
            total_revenue=total_revenue,
        )

    # CUSTOMER DASHBOARD
    orders = (
        Order.query
        .filter_by(user_id=user_id)
        .order_by(Order.created_at.desc())
        .all()
    )
    recent_orders = orders[:2]

    total_products = Product.query.filter_by(is_active=True).count()
    total_categories = db.session.query(Product.category).distinct().count()

    latest_products = (
        Product.query
        .filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .limit(6)
        .all()
    )

    if orders and orders[0].product:
        last_cat = orders[0].product.category
        recommended = (
            Product.query
            .filter_by(category=last_cat, is_active=True)
            .limit(6)
            .all()
        )
    else:
        recommended = (
            Product.query
            .filter_by(is_active=True)
            .order_by(Product.price.desc())
            .limit(6)
            .all()
        )

    return render_template(
        "dashboards/customer_dashboard.html",
        recent_orders=recent_orders,
        total_orders=len(orders),
        total_products=total_products,
        total_categories=total_categories,
        latest_products=latest_products,
        recommended_products=recommended,
    )
