# routes/orders.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from models import db
from models.order import Order
from models.product import Product
from models.user import User
from utils.decorators import login_required, role_required

orders_bp = Blueprint("orders", __name__)


# -----------------------------------------------------------
# CUSTOMER: PLACE ORDER
# -----------------------------------------------------------
@orders_bp.route("/orders/place/<int:product_id>", methods=["POST"])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)

    if not product.is_active:
        flash("This product is not available.", "danger")
        return redirect(url_for("products.product_details", product_id=product_id))

    user_id = session.get("user_id")

    try:
        quantity = int(request.form.get("quantity", 1))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        quantity = 1

    if product.stock is not None and product.stock < quantity:
        flash("Not enough stock available.", "danger")
        return redirect(url_for("products.product_details", product_id=product_id))

    order = Order(
        user_id=user_id,
        product_id=product_id,
        quantity=quantity,
        status="Pending",
    )

    if product.stock is not None:
        product.stock -= quantity

    db.session.add(order)
    db.session.commit()

    flash("Order placed successfully!", "success")
    return redirect(url_for("orders.my_orders"))


# -----------------------------------------------------------
# CUSTOMER: VIEW OWN ORDERS
# -----------------------------------------------------------
@orders_bp.route("/orders/my")
@login_required
def my_orders():
    user_id = session.get("user_id")

    orders = (
        Order.query
        .filter_by(user_id=user_id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template("orders/my_orders.html", orders=orders)


# -----------------------------------------------------------
# SELLER: VIEW ORDERS FOR HIS PRODUCTS ONLY
# -----------------------------------------------------------
@orders_bp.route("/seller/orders")
@login_required
@role_required("seller")
def seller_orders():
    seller_id = session.get("user_id")

    orders = (
        Order.query
        .join(Product)
        .filter(Product.seller_id == seller_id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template("orders/seller_orders.html", orders=orders)


# -----------------------------------------------------------
# SELLER: UPDATE ORDER STATUS (Pending / Shipped / Delivered)
# -----------------------------------------------------------
@orders_bp.route("/seller/orders/<int:order_id>/update", methods=["POST"])
@login_required
@role_required("seller")
def update_order_status(order_id):
    seller_id = session.get("user_id")
    order = Order.query.get_or_404(order_id)

    # Ensure this order belongs to this seller's product
    if not order.product or order.product.seller_id != seller_id:
        flash("You cannot update this order.", "danger")
        return redirect(url_for("orders.seller_orders"))

    status = request.form.get("status", "Pending")
    if status not in ["Pending", "Shipped", "Delivered"]:
        status = "Pending"

    order.status = status
    db.session.commit()

    flash("Order status updated!", "success")
    return redirect(url_for("orders.seller_orders"))


# -----------------------------------------------------------
# SELLER: DELETE ORDER (Only their own product orders)
# -----------------------------------------------------------
@orders_bp.route("/seller/orders/<int:order_id>/delete")
@login_required
@role_required("seller")
def delete_seller_order(order_id):
    seller_id = session.get("user_id")
    order = Order.query.get_or_404(order_id)

    if not order.product or order.product.seller_id != seller_id:
        flash("You cannot delete another seller's order.", "danger")
        return redirect(url_for("orders.seller_orders"))

    db.session.delete(order)
    db.session.commit()

    flash("Order deleted.", "success")
    return redirect(url_for("orders.seller_orders"))
