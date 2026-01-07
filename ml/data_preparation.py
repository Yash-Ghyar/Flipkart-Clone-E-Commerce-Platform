# ml/data_preparation.py

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # project root
DB_PATH = os.path.join(BASE_DIR, "ecommerce.db")
INTERACTIONS_CSV = os.path.join(os.path.dirname(__file__), "interactions.csv")

def export_interactions():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)

    # "order" table name is reserved word, so quote it
    query = 'SELECT customer_id, product_id FROM "order"'
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.to_csv(INTERACTIONS_CSV, index=False)
    print(f"[ML] Exported interactions to {INTERACTIONS_CSV}")
    print(df.head())

if __name__ == "__main__":
    export_interactions()