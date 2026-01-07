# routes/admin.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from models import db
from models.user import User
from models.product import Product
from models.order import Order
from utils.decorators import login_required, role_required

admin_bp = Blueprint("admin", __name__)


# -----------------------------------------------------------
# ADMIN DASHBOARD  →  /admin/admin/dashboard   (because of url_prefix)
# -----------------------------------------------------------
@admin_bp.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()

    return render_template(
        "dashboards/admin_dashboard.html",
        total_users=total_users,
        total_products=total_products,
        total_orders=total_orders,
    )


# -----------------------------------------------------------
# ADMIN: MANAGE USERS  →  /admin/admin/users
# -----------------------------------------------------------
@admin_bp.route("/admin/users")
@login_required
@role_required("admin")
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("products/admin_users.html", users=users)


# change role (customer/seller/admin)
@admin_bp.route("/admin/users/<int:user_id>/role", methods=["POST"])
@login_required
@role_required("admin")
def admin_change_user_role(user_id):
    user = User.query.get_or_404(user_id)
    current_admin_id = session.get("user_id")

    new_role = request.form.get("role", "").strip().lower()

    # only valid roles
    if new_role not in ["customer", "seller", "admin"]:
        flash("Invalid role selected.", "danger")
        return redirect(url_for("admin.admin_users"))

    # do not allow admin to change his own role
    if user.id == current_admin_id:
        flash("You cannot change your own role.", "warning")
        return redirect(url_for("admin.admin_users"))

    user.role = new_role
    db.session.commit()

    flash("User role updated successfully.", "success")
    return redirect(url_for("admin.admin_users"))


# delete user
@admin_bp.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    current_admin_id = session.get("user_id")

    # do not allow admin to delete himself
    if user.id == current_admin_id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin.admin_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("admin.admin_users"))


# -----------------------------------------------------------
# ADMIN: MANAGE PRODUCTS  → /admin/admin/products
# -----------------------------------------------------------
@admin_bp.route("/admin/products")
@login_required
@role_required("admin")
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("products/admin_products.html", products=products)


# -----------------------------------------------------------
# ADMIN: VIEW ALL ORDERS  → /admin/admin/orders
# -----------------------------------------------------------
@admin_bp.route("/admin/orders")
@login_required
@role_required("admin")
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    products = {p.id: p for p in Product.query.all()}
    users = {u.id: u for u in User.query.all()}

    return render_template(
        "products/admin_orders.html",
        orders=orders,
        products=products,
        users=users,
    )
