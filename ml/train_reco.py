# ml/train_reco.py

import os
import itertools
import pickle
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
INTERACTIONS_CSV = os.path.join(os.path.dirname(__file__), "interactions.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "reco_model.pkl")

def train_recommender(min_cooccurrence: int = 1, top_k: int = 10):
    if not os.path.exists(INTERACTIONS_CSV):
        raise FileNotFoundError(
            f"Interactions file not found at: {INTERACTIONS_CSV}. "
            f"Run data_preparation.py first."
        )

    df = pd.read_csv(INTERACTIONS_CSV)

    if df.empty:
        print("[ML] No interactions found. Train after some orders are placed.")
        return

    # group products per customer
    user_products = (
        df.groupby("customer_id")["product_id"]
        .apply(list)
        .reset_index()
    )

    co_counts = {}

    for _, row in user_products.iterrows():
        products = list(set(row["product_id"]))
        if len(products) < 2:
            continue

        for p1, p2 in itertools.combinations(sorted(products), 2):
            co_counts.setdefault(p1, {})
            co_counts.setdefault(p2, {})

            co_counts[p1][p2] = co_counts[p1].get(p2, 0) + 1
            co_counts[p2][p1] = co_counts[p2].get(p1, 0) + 1

    similar_products = {}

    for p, neighbors in co_counts.items():
        filtered = [(q, c) for q, c in neighbors.items() if c >= min_cooccurrence]
        filtered.sort(key=lambda x: x[1], reverse=True)
        similar_products[p] = [q for q, _ in filtered[:top_k]]

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(similar_products, f)

    print(f"[ML] Saved recommender model to {MODEL_PATH}")
    # print few examples
    for k, v in list(similar_products.items())[:5]:
        print(f"Product {k} → similar: {v}")

if __name__ == "__main__":
    train_recommender()
