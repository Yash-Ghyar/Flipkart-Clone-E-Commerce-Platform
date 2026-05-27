🛒 Flipkart Clone — AI-Powered Full Stack E-Commerce Platform
Intelligent Multi-Role E-Commerce System with Machine Learning Recommendations

A production-inspired full-stack e-commerce platform designed to simulate real-world online marketplaces.

Built using Flask, SQLAlchemy, HTML/CSS, Bootstrap, and Machine Learning, the application enables seamless shopping experiences through dedicated Customer, Seller, and Admin portals, integrated with an intelligent recommendation engine.

The system follows a modular architecture with secure authentication, scalable backend design, and dynamic user interaction.

🚀 Project Overview

This platform replicates core functionalities of modern e-commerce applications by combining:

✅ Customer Shopping Experience
✅ Seller Product Management
✅ Administrative Control Panel
✅ AI-Based Recommendation Engine
✅ Secure Role-Based Access System

✨ Features
👤 Customer Portal
Secure Registration & Login
Browse Complete Product Catalog
Search Products & Category Filtering
Product Details View
Place Orders
Order Tracking System
View Order History
Personalized Product Recommendations
Responsive Customer Dashboard
🛍️ Seller Portal
Seller Registration & Authentication
Add New Products
Edit Existing Listings
Delete Products
Product Image Upload
Manage Customer Orders
Update Delivery Status:
Pending
Shipped
Delivered
🛠️ Admin Control Panel
Restricted Admin Access
User Management System
Role Assignment
Product Monitoring
Order Management
Platform Analytics Dashboard
System Statistics Overview
🤖 Intelligent Recommendation System

Implemented a Hybrid Multi-Level Recommendation Architecture to ensure recommendation continuity.

Level 1 — Machine Learning Recommendation

Generates personalized product suggestions using trained recommendation models.

Level 2 — Category Similarity Recommendation

Recommends relevant products from similar categories.

Level 3 — Trending Product Engine

Displays recently popular products when ML predictions are unavailable.

Result:

Improved recommendation availability and better simulated shopping personalization.

🏗️ System Architecture
User
 ↓
Frontend (HTML + Bootstrap + Jinja2)
 ↓
Flask Application
 ↓
Business Logic Layer
 ↓
SQLAlchemy ORM
 ↓
Database

Recommendation Engine
 ↓
ML Model (.pkl)
 ↓
Personalized Suggestions
💻 Tech Stack
Frontend
HTML5
CSS3
Bootstrap 5
Jinja2
Backend
Flask
SQLAlchemy
Flask Blueprints
Database
SQLite
Machine Learning
Python
Recommendation System
Security
Password Hashing
Route Protection
Role-Based Access
🔐 Security Implementation
Secure Password Encryption using Werkzeug
Authentication & Authorization
Protected Admin Routes
Role-Based Access Control
Secure File Upload Validation
📂 Project Structure
Flipkart-Clone/
│
├── app/
│ ├── routes/
│ ├── models/
│ ├── services/
│ └── templates/
│
├── static/
├── uploads/
├── recommendation/
├── reco_model.pkl
├── requirements.txt
├── app.py
└── README.md
⚙️ Installation
git clone <repository-url>

cd Flipkart-Clone

pip install -r requirements.txt

python create_db.py

python app.py

Run:

http://127.0.0.1:5000
📈 Future Enhancements
Payment Gateway Integration
Wishlist & Cart Optimization
Cloud Deployment
Docker Containerization
Analytics Dashboard
Real-Time Notifications
Recommendation Model Optimization
👨‍💻 Author

Yash Ghyar
BTech — Artificial Intelligence & Data Science
VIIT Pune
