# 🛒 Flipkart Clone

### AI-Powered Full Stack E-Commerce Platform

🚀 **Live Demo:** https://flipkart-clone-e-commerce-platform.vercel.app/

---

## 📌 Overview

A production-inspired full-stack e-commerce platform designed to simulate real-world online marketplaces.

Built using Flask, SQLAlchemy, Bootstrap, and Machine Learning, the application provides dedicated Customer, Seller, and Admin portals along with an intelligent recommendation engine for personalized shopping experiences.

The project demonstrates full-stack web development, role-based authentication, database management, and recommendation system implementation in a single integrated platform.

---

## 🚀 Features

### 👤 Customer Portal

✅ Secure Registration & Login

✅ Browse Complete Product Catalog

✅ Search & Category Filtering

✅ Product Detail View

✅ Place Orders

✅ Order Tracking System

✅ Order History Management

✅ Personalized Product Recommendations

✅ Responsive Customer Dashboard

---

### 🛍️ Seller Portal

✅ Seller Registration & Authentication

✅ Add New Products

✅ Update Existing Products

✅ Delete Products

✅ Product Image Upload

✅ Manage Customer Orders

✅ Update Delivery Status

* Pending
* Shipped
* Delivered

---

### 🛠️ Admin Portal

✅ Restricted Admin Access

✅ User Management System

✅ Role Assignment

✅ Product Monitoring

✅ Order Management

✅ Platform Analytics Dashboard

✅ System Statistics Overview

---

## 🤖 Intelligent Recommendation System

Implemented a Hybrid Multi-Level Recommendation Architecture.

### Level 1 — Machine Learning Recommendation

Generates personalized product recommendations using trained ML models.

### Level 2 — Category Similarity Recommendation

Suggests relevant products from similar categories.

### Level 3 — Trending Product Engine

Displays popular products when ML recommendations are unavailable.

### Result

✅ Improved Recommendation Availability

✅ Better Shopping Personalization

✅ Enhanced User Experience

---

## 🏗️ System Architecture

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

SQLite Database

↓

Recommendation Engine
↓

ML Model (.pkl)
↓

Personalized Product Suggestions

---

## 🛠 Tech Stack

### Backend

* Python
* Flask
* SQLAlchemy
* Flask Blueprints

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2

### Database

* SQLite

### Machine Learning

* Recommendation System
* Hybrid Recommendation Engine

### Security

* Password Hashing
* Authentication & Authorization
* Role-Based Access Control

---

## 🔐 Security Features

✅ Secure Password Encryption using Werkzeug

✅ Authentication & Authorization

✅ Protected Admin Routes

✅ Role-Based Access Control

✅ Secure File Upload Validation

---

## 📂 Project Structure

```text
Flipkart-Clone/
│
├── app.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── templates/
│
├── static/
├── uploads/
├── recommendation/
│   └── reco_model.pkl
│
└── screenshots/
```

---

## 💻 Installation

### Clone Repository

```bash
git clone https://github.com/Yash-Ghyar/Flipkart-Clone.git
```

### Navigate to Project Directory

```bash
cd Flipkart-Clone
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

```bash
python create_db.py
```

### Run Application

```bash
python app.py
```

### Open Browser

```bash
http://127.0.0.1:5000
```

---

## 🌟 Project Highlights

✅ Full Stack E-Commerce Platform

✅ Machine Learning Recommendation Engine

✅ Multi-Role Authentication System

✅ Customer, Seller & Admin Dashboards

✅ Product & Order Management

✅ Industry-Oriented Architecture

✅ Resume-Ready AI Project

---

## 📈 Future Enhancements

* Payment Gateway Integration
* Wishlist & Cart Optimization
* Cloud Deployment
* Docker Containerization
* Analytics Dashboard
* Real-Time Notifications
* Recommendation Model Optimization

---

## 👨‍💻 Author

**Yash Ghyar**

🎓 B.Tech – Artificial Intelligence & Data Science

🏫 Vishwakarma Institute of Information Technology (VIIT), Pune

---

## 🔗 Connect With Me

### GitHub

https://github.com/Yash-Ghyar

### LinkedIn

https://linkedin.com/in/yash-ghyar-94b58825b
