# ☕ B-Cafe API Project

Welcome to **B-Cafe**, a Django REST Framework-based API project designed to manage the menu and reservation system for a modern café-restaurant.

## 🧩 Overview

This project provides a structured and scalable backend system that handles:

- 🍽️ **Café and Restaurant Menu**:  
  Manage categories (food, drinks, desserts, etc.) and detailed information for each product/item.

- 📅 **Table Reservation System**:  
  Customers can reserve tables without logging in, and automatic notifications/messages are sent to both the customer and the admin upon successful reservation.

- 📞 **Contact & Info Pages**:  
  Includes an About Us and Contact Us section for displaying café information and handling user communication.

- 🔍 **Search & Filter Functionality**:  
  Powerful search and filter support across API endpoints using Django REST Framework's `filter_backends`.

- ⚙️ **App Modularization**:  
  The project is split into multiple Django apps to ensure clarity, scalability, and ease of extension.

## 🔧 Features

- ✅ Built with **Django REST Framework**
- ✅ Clean and RESTful API design
- ✅ Custom **signals** to handle actions like sending notifications after reservations
- ✅ Robust **validators** to ensure data integrity (e.g., phone numbers, guest limits, item availability)
- ✅ Admin-only access to sensitive endpoints using custom permissions
- ✅ Advanced **filtering and searching** capabilities using `DjangoFilterBackend` and `SearchFilter`
- ✅ **Dockerized** for easy deployment and environment setup

## 📦 Technologies Used

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- Django Filters  
- Docker & Docker Compose  

## 📁 Apps Structure

- `menu`: Handles categories and café menu items  
- `reservation`: Manages table reservations and related messaging  
- `info`: Provides café/restaurant contact and general information (like *About Us* and *Contact Us*)  
- `utility`: Common base views, custom permissions, and helpers  

## 🚀 Getting Started
### Backend Setup

```bash
git clone <repo-url>
cd B-Cofe
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Crafted with ❤️ by Behnoushin (Behnoush Shahraeini)
