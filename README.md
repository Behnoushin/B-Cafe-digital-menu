# ☕ B-Cafe API Project

Welcome to **B-Cafe**, a Django REST Framework-based API project designed to manage the menu and reservation system for a modern café-restaurant.

## 🧩 Overview

This project provides a structured and scalable backend system that handles:

- 🍽️ **Café and Restaurant Menu**:  
  Manage categories (food, drinks, desserts, etc.) and detailed information for each product/item.

- 📅 **Table Reservation System**:  
  Customers can reserve tables, and upon reservation, automatic notifications/messages are sent to both the customer and the admin.

- ⚙️ **App Modularization**:  
  The project is split into multiple Django apps to ensure clarity, scalability, and ease of extension.

## 🔧 Features

- ✅ Built with **Django REST Framework**
- ✅ Clean and RESTful API design
- ✅ Custom **signals** to handle actions like sending notifications after orders/reservations
- ✅ Robust **validators** to ensure data integrity (e.g., phone numbers, item availability)
- ✅ Admin-only access to sensitive endpoints using custom permissions
- ✅ **Dockerized** for easy deployment and environment setup

## 📦 Technologies Used

- Python 3.x
- Django 4.x
- Django REST Framework
- Docker & Docker Compose

## 📁 Apps Structure

- `menu`: Handles categories and café menu items
- `reservation`: Manages table reservations and related messaging
- `order`: Processes customer orders
- `utility`: Common base views, custom permissions, and helpers

## 🚀 Getting Started

To run this project using Docker:

```bash
docker-compose up --build
