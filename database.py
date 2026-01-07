# database.py
from flask_sqlalchemy import SQLAlchemy

# Single global SQLAlchemy instance used across models
db = SQLAlchemy()
