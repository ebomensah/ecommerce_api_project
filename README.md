Hypersale eCommerce API

Overview
Hypersale is a full-fledged eCommerce API built with Django and Django Rest Framework (DRF), providing a platform where users can manage products, orders, reviews, wishlists, and discounts. The system supports user authentication and user-specific actions (like adding items to a wishlist, creating orders, and submitting reviews).

Features
Product Management: Users can view products, search by name, category, price, and stock.
Order Management: Users can create and view orders, including product details and quantities.
Wishlist Functionality: Users can add and remove items from their wishlists.
Reviews: Users can write and manage reviews for products.
Discounts: Allows admins to create discounts linked to specific products.
Authentication: All actions require users to be authenticated through Django's built-in user system.
CSRF and Security: The system uses CSRF tokens for protection and ensures secure POST requests.

Project Setup
Requirements
Python 3.9+
Django 5.1+
Django Rest Framework (DRF)
Additional libraries like django-filter for filtering and django-cors-headers for handling cross-origin requests.

Installation
Clone the Repository:

git clone https://github.com/ebomensah/e-commerce.git
cd hypersale

Create a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies:
pip install -r requirements.txt

Apply Database Migrations:
python manage.py migrate

Create a Superuser (for admin access):
python manage.py createsuperuser

Start the Development Server:
python manage.py runserver

Endpoints
Auth Endpoints
POST /api/login/ - User login
POST /api/logout/ - User logout
POST /api/register/ - User registration

Product Endpoints
GET /api/products/ - List all products
POST /api/products/ - Add a new product
GET /api/products/<id>/ - View product details
PUT /api/products/<id>/ - Update product details
DELETE /api/products/<id>/ - Delete a product
Order Endpoints
GET /api/orders/ - List orders of the logged-in user
POST /api/orders/ - Create a new order
GET /api/orders/<id>/ - View details of a specific order
Wishlist Endpoints
GET /api/wishlist/ - List the logged-in user’s wishlist
POST /api/wishlist/ - Add product to the wishlist
DELETE /api/wishlist/<id>/ - Remove product from the wishlist
Review Endpoints
GET /api/reviews/ - List all reviews (filterable by product/user)
POST /api/reviews/ - Add a new review to a product
GET /api/reviews/<id>/ - View a specific review
Discount Endpoints
GET /api/discounts/ - List all discounts created by the logged-in user
POST /api/discounts/ - Create a new discount for a product
GET /api/discounts/<id>/ - View details of a specific discount
Root Endpoint (API Home)
GET /api/ - Overview of all available endpoints

How to Contribute
Fork the repository and clone it to your local machine.
Create a branch for your feature or bugfix (git checkout -b feature-xyz).
Make your changes and commit them (git commit -m "Implement ABC").
Push the changes to your fork (git push origin feature-xyz).
Open a Pull Request to the main branch of the original repository.