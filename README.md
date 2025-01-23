# Shoplit API Documentation

## Overview
The Shoplit API is a backend service for an e-commerce platform. It allows users to interact with product data, categories, and subcategories via RESTful endpoints. The API is built using Django and Django REST Framework (DRF).
Deployed Version: https://shoplit-prod-74e250e64c74.herokuapp.com
Api Documentation: https://shoplit-prod-74e250e64c74.herokuapp.com/swagger-ui/

## Features
- Manage product categories and subcategories.
- Create, read, update, and delete products.
- Search and filter products.
- User authentication and authorization (token based JWT authentication).
- Rate limiting to endpoints
- Caching 


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

