# Shoplit API Documentation

## Overview
The Shoplit API is a backend service for an e-commerce platform. It allows users to interact with product data, categories, and subcategories via RESTful endpoints. The API is built using Django and Django REST Framework (DRF).

Deployed Version: https://shoplit-prod-74e250e64c74.herokuapp.com

Api Documentation: https://shoplit-prod-74e250e64c74.herokuapp.com/swagger-ui/

## Features

### User Management
- **User Registration**: Create user accounts.
- **User Authentication**: Login/logout functionality with token-based authentication.
- **Password Reset**: Reset forgotten passwords via email.
- **User Profiles**: View and update user information.

### Product Management
- **Product Listings**: Fetch a list of all available products.
- **Product Details**: Retrieve detailed information for a specific product.
- **Category & Subcategory Management**: Filter products by category or subcategory.
- **Product Search**: Search for products by name or description.

### Cart Management
- **Add to Cart**: Add products to a shopping cart.
- **View Cart**: Retrieve items in the user’s cart.
- **Update Cart**: Adjust quantities of products in the cart.
- **Remove from Cart**: Delete items from the cart.

### Order Management
- **Place Orders**: Checkout and place orders for products in the cart.
- **Order History**: View all orders placed by a user.
- **Order Details**: Fetch detailed information about a specific order.

### Payment Integration
- **Payment Gateway**: Integration with paystack.
- **Order Payment Status**: Update and track payment status of orders.


### Wishlist
- **Add to Wishlist**: Save products for later purchase.
- **View Wishlist**: Fetch the user’s wishlist items.
- **Remove from Wishlist**: Delete items from the wishlist.

### Reviews and Ratings
- **Product Reviews**: Allow users to leave reviews and ratings for products.
- **Review Moderation**: Approve or reject reviews for public display.
- **Review Display**: Fetch all reviews for a specific product.

### Admin Features

### Notifications
- **Order Status Updates**: Notify users about order status changes via in app and SMS.
- **Promotional Notifications**: Send updates about sales, discounts, or new arrivals.

### SMS Notifications
- **Order Updates**: Notify users via SMS about their order status (e.g., confirmed, shipped, delivered).
- **Promotions**: Send promotional offers and updates directly to users' phones.



## Prerequisites
To run the API locally, ensure you have the following installed:
- Python 3.9+
- Django
- Django REST Framework
- MySQL (or any database supported by Django)
- Use the requirements.txt file

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Andrew-oduola/shoplit.git
   cd shoplit
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     SECRET_KEY=your_secret_key
     DEBUG=True
     ALLOWED_HOSTS=localhost, 127.0.0.1
     DATABASE_URL=your_database_url
     ```

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```



## API Endpoints

### Products
#### List All Products
**GET** `/api/products/`

Response:
```json
[
    {
        "id": 1,
        "name": "Product Name",
        "description": "Product description",
        "price": 29.99,
        "category": "Category Name",
        "subcategory": "Subcategory Name"
    },
    ...
]
```

#### Retrieve a Single Product
**GET** `/api/products/<id>/`

Response:
```json
{
    "id": 1,
    "name": "Product Name",
    "description": "Product description",
    "price": 29.99,
    "category": "Category Name",
    "subcategory": "Subcategory Name"
}
```

#### Create a Product
**POST** `/api/products/`

Request:
```json
{
    "name": "New Product",
    "description": "New product description",
    "price": 19.99,
    "category": "Category Name",
    "subcategory": "Subcategory Name"
}
```

Response:
```json
{
    "id": 2,
    "name": "New Product",
    "description": "New product description",
    "price": 19.99,
    "category": "Category Name",
    "subcategory": "Subcategory Name"
}
```

#### Update a Product
**PUT** `/api/products/<id>/`

Request:
```json
{
    "name": "Updated Product",
    "description": "Updated product description",
    "price": 24.99
}
```

Response:
```json
{
    "id": 1,
    "name": "Updated Product",
    "description": "Updated product description",
    "price": 24.99
}
```

#### Delete a Product
**DELETE** `/api/products/<id>/`

Response:
```json
{
    "message": "Product deleted successfully."
}

### Categories
#### List All Categories
**GET** `/api/categories/`

Response:
```json
[
    {
        "id": 1,
        "name": "Category Name",
        "description": "Category description"
    },
    ...
]
```

#### Create a Category
**POST** `/api/categories/`

Request:
```json
{
    "name": "New Category",
    "description": "New category description"
}
```

Response:
```json
{
    "id": 2,
    "name": "New Category",
    "description": "New category description"
}
```

### Subcategories
#### List All Subcategories
**GET** `/api/subcategories/`

Response:
```json
[
    {
        "id": 1,
        "name": "Subcategory Name",
        "category": "Category Name"
    },
    ...
]
```

## Deployment
To deploy on Heroku:
1. Log in to Heroku:
   ```bash
   heroku login
   ```

2. Create a Heroku app:
   ```bash
   heroku create shoplit
   ```

3. Add Heroku Postgres:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Push to Heroku:
   ```bash
   git push heroku main
   ```

5. Run migrations on Heroku:
   ```bash
   heroku run python manage.py migrate
   ```

6. Open the app:
   ```bash
   heroku open
   ```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to your branch: `git push origin feature-name`.
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to modify and expand this README to fit your project’s specific details and requirements.

