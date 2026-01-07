# create_db.py

from app import create_app
from models import db

# Import all models so SQLAlchemy knows them
from models.user import User
from models.product import Product
from models.order import Order

app = create_app()

with app.app_context():
    print("⛔ Dropping existing database tables...")
    db.drop_all()

    print("📦 Creating new database tables...")
    db.create_all()

    print("✅ Database reset successfully!")
