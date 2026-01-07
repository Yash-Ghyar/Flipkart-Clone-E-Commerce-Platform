# ml/recommender.py

import pickle

# Load ML model if available
try:
    model = pickle.load(open("ml/reco_model.pkl", "rb"))
except:
    print("⚠ ML model not found. Using fallback recommender.")
    model = None


def get_recommendations(product, limit=6):
    """
    Returns recommended products:
    1. ML-based recommendations (if model exists)
    2. Fallback: category-based recommendations
    """

    from models.product import Product

    if not product:
        return []

    # ---------------------------------------------
    # 1️⃣ ML MODEL RECOMMENDATIONS
    # ---------------------------------------------
    try:
        if model and hasattr(model, "get"):
            recommended_ids = model.get(product.id, [])

            if recommended_ids:
                recos = (
                    Product.query
                    .filter(Product.id.in_(recommended_ids))
                    .filter_by(is_active=True)
                    .all()
                )

                if len(recos) >= 3:   # enough results?
                    return recos[:limit]

    except Exception as e:
        print("⚠ ML Model Error:", e)

    # ---------------------------------------------
    # 2️⃣ FALLBACK: CATEGORY-BASED SIMILAR PRODUCTS
    # ---------------------------------------------
    fallback = (
        Product.query
        .filter(Product.category == product.category)
        .filter(Product.id != product.id)
        .filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .limit(limit)
        .all()
    )

    if fallback:
        return fallback

    # ---------------------------------------------
    # 3️⃣ FINAL FALLBACK (ANY TRENDING PRODUCTS)
    # ---------------------------------------------
    return (
        Product.query
        .filter_by(is_active=True)
        .order_by(Product.created_at.desc())
        .limit(limit)
        .all()
    )
