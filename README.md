📦 Flipkart Clone – Full Stack E-Commerce Platform
(Flask Backend + HTML/CSS + Bootstrap Frontend + SQLAlchemy + ML)

A complete full-stack e-commerce web application built using Flask (Backend) and HTML, CSS, Bootstrap (Frontend) with a SQLAlchemy ORM and ML-based Product Recommendation System.
Includes Customer Portal, Seller Portal, and Admin Panel.

🚀 Key Features
👤 Customer Features

Customer register/login

Browse all products + search + category filter

View product details

Add orders

My Orders page

Track order status

Smart recommendations using ML + fallback

Clean customer dashboard

🛒 Seller Features

Seller register/login

Add / Edit / Delete products

Upload product images

View customer orders for their products

Update order status (Pending → Shipped → Delivered)

Delete orders

🛠️ Admin Features

Secret admin registration page (localhost-only)

View & manage all users

Change user roles (customer / seller / admin)

Delete users

Manage all products

Manage all orders

Admin dashboard with system stats

🎨 Frontend (HTML + CSS + Bootstrap)

The entire UI is built using:

HTML5

CSS3

Bootstrap 5

Responsive components & cards

Clean, modern Flipkart-style layout

All pages use Jinja2 templates for dynamic rendering.

💻 Backend (Flask + SQLAlchemy)

Flask app factory pattern

SQLAlchemy ORM models

Route-based Blueprints for users, products, orders, admin

Secure password hashing

Role-based route protection

Image upload handling

🤖 Recommendation Engine (Machine Learning)
Works in 3 Levels:

1️⃣ ML-based recommendations (if reco_model.pkl exists)
2️⃣ Category-based fallback recommendations
3️⃣ Latest trending products fallback

Guarantees meaningful product suggestions every time.

🔐 Security

Password hashing using Werkzeug

Authenticated + role-restricted routes

Secure image file handling

Admin route protected by IP restriction

⚙️ How to Run the Project
1️⃣ Install requirements
pip install -r requirements.txt

2️⃣ Create the database
python
from app import app
from models import db
with app.app_context():
    db.create_all()

3️⃣ Start the application
python app.py


Visit: http://127.0.0.1:5000
=======
# Flipkart-Clone-E-Commerce-Platform
>>>>>>> 2c68d290a20b91e35c7022da8bb9ed130d4ce092
