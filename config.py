# config.py
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Change this in production → use env var
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-change-me")

    # SQLite DB in project root
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "ecommerce.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads (product images)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "images")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max per file

    # You can add more app-level config here later
