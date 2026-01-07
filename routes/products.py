# routes/products.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from models import db
from models.product import Product
from models.order import Order
from models.user import User

from utils.decorators import login_required, role_required
from utils.image_handler import save_image

# ML recommendations
from ml.recommender import get_recommendations

products_bp = Blueprint("products", __name__)


# -----------------------------------------------------------
# PUBLIC: PRODUCT LIST PAGE (Flipkart-style)
# -----------------------------------------------------------
@products_bp.route("/products")
def product_list():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")

    query = Product.query.filter_by(is_active=True)

    if q:
        like = f"%{q}%"
        query = query.filter(Product.name.ilike(like))

    if category:
        query = query.filter(Product.category == category)

    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.all()

    # All categories
    categories_raw = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories_raw]

    return render_template(
        "products/product_list.html",
        products=products,
        categories=categories,
        q=q,
        current_category=category,
        sort=sort,
    )


# -----------------------------------------------------------
# PUBLIC: PRODUCT DETAILS + ML RECOMMENDATIONS
# -----------------------------------------------------------
@products_bp.route("/product/<int:product_id>")
def product_details(product_id):
    product = Product.query.get_or_404(product_id)

    # product inactive → don't show
    if not product.is_active:
        flash("This product is no longer available.", "warning")
        return redirect(url_for("products.product_list"))

    # ML recommendations
    recos = get_recommendations(product, limit=6)

    return render_template(
        "products/product_details.html",
        product=product,
        recos=recos,
    )


# -----------------------------------------------------------
# SELLER / ADMIN: ADD PRODUCT
# -----------------------------------------------------------
@products_bp.route("/seller/products/add", methods=["GET", "POST"])
@login_required
@role_required("seller", "admin")
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        price_raw = request.form.get("price", "0")
        stock_raw = request.form.get("stock", "0")

        try:
            price = float(price_raw)
        except ValueError:
            price = 0

        try:
            stock = int(stock_raw)
        except ValueError:
            stock = 0

        if not name or not category or price <= 0:
            flash("Name, category and valid price required!", "danger")
            return render_template("products/add_product.html")

        # Save image
        image_file = request.files.get("image")
        filename = save_image(image_file)

        product = Product(
            name=name,
            category=category,
            price=price,
            stock=stock,
            description=description,
            image_filename=filename,
            seller_id=session.get("user_id"),
            is_active=True,
        )

        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("users.dashboard"))

    return render_template("products/add_product.html")


# -----------------------------------------------------------
# SELLER / ADMIN: EDIT PRODUCT
# -----------------------------------------------------------
@products_bp.route("/seller/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("seller", "admin")
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    current_user = session.get("user_id")
    role = session.get("role")

    # Seller cannot edit someone else’s product
    if role == "seller" and product.seller_id != current_user:
        flash("You can edit only your own products!", "danger")
        return redirect(url_for("users.dashboard"))

    if request.method == "POST":
        product.name = request.form.get("name", "").strip()
        product.category = request.form.get("category", "").strip()
        product.description = request.form.get("description", "").strip()

        # Price / Stock update
        try:
            product.price = float(request.form.get("price", "0"))
        except:
            product.price = 0

        try:
            product.stock = int(request.form.get("stock", "0"))
        except:
            product.stock = 0

        # New image?
        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = save_image(image_file)
            if filename:
                product.image_filename = filename

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("products.product_details", product_id=product.id))

    return render_template("products/edit_product.html", product=product)


# -----------------------------------------------------------
# SELLER / ADMIN: DELETE (soft delete)
# -----------------------------------------------------------
@products_bp.route("/seller/products/<int:product_id>/delete")
@login_required
@role_required("seller", "admin")
def seller_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    current_user = session.get("user_id")
    role = session.get("role")

    # Seller cannot delete others' products
    if role == "seller" and product.seller_id != current_user:
        flash("You can delete only your own products!", "danger")
        return redirect(url_for("users.dashboard"))

    product.is_active = False
    db.session.commit()

    flash("Product removed (soft delete).", "success")
    return redirect(url_for("users.dashboard"))
