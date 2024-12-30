from locust import HttpUser, task, between
from rest_framework import status
import random
from pprint import pprint
import os 
import django
from decimal import Decimal

from faker import Faker


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoplit.settings")
# load the Django apps registry
django.setup()

fake = Faker()

class EcommerceUser(HttpUser):
    wait_time = between(1, 3)
    products_ids = []
    categories_ids = []
    subcategories_ids = []

    def on_start(self):
        # Pre-fectch the ids of the products to be used in the test
        response = self.client.get("/api/products")
        

        login_response = self.client.post("/auth/jwt/create", {
        "email": "ayobamioduola13@gmail.com",
        "password": "secret",
        })

        self.token = login_response.json()["access"]
        self.headers  = {"Authorization": f"JWT {self.token}", 'content-type': 'application/json'}
        self.auth = ('ayobamioduola13@gmail.com', 'secret')

        self.client.headers.update(self.headers)

        # pprint(login_response.json())

        # headers =  {
        #     "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NTkzNDUzLCJpYXQiOjE3MzU1MDcwNTMsImp0aSI6ImFlMDBkODlhYmZmMTRjYmRhMTczZDM3YTllMzMzZTMzIiwidXNlcl9pZCI6IjM2MDY4ZTQyLWZhNTktNDdmMS1iOWNhLWViMjU5YjE5MDcyYiJ9.IDX7b_NCY3YiJMhUGOOi0UDvDeLx1q3mrtsuUmyCHyM"
        # }

        # self.client.headers = {
        #     "Authorization": "JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1NTkzNDUzLCJpYXQiOjE3MzU1MDcwNTMsImp0aSI6ImFlMDBkODlhYmZmMTRjYmRhMTczZDM3YTllMzMzZTMzIiwidXNlcl9pZCI6IjM2MDY4ZTQyLWZhNTktNDdmMS1iOWNhLWViMjU5YjE5MDcyYiJ9.IDX7b_NCY3YiJMhUGOOi0UDvDeLx1q3mrtsuUmyCHyM"
        # }

        response_cart = self.client.get("/api/cart", 
                                        headers=self.headers,
                                        name="/api/cart",
                                        auth=self.auth)
        cart_result = response_cart.json()


        if response_cart.status_code == status.HTTP_200_OK:
            
            self.cart_id = cart_result.get('id')  # Extract cart ID if present
            # print(f"Cart ID: {self.cart_id}")
        else:
            print("Failed to fetch cart")
            print(response_cart.status_code)
            # pprint(cart_result)
        # self.cart_id = cart_result['id']


        data = response.json()
        if response.status_code == status.HTTP_200_OK:
            self.products_ids = [product["id"] for product in data['results']]
            self.categories_ids = [product["category"] for product in data['results']]
            self.subcategories_ids = [product["subcategory"] for product in data['results']]
        else:
            print("Failed to fetch products")

        
    
    # create cart for user so it can be referenced later on
    

    @task(2)
    def view_products(self):
        self.client.get("/api/products", name="/api/products")

    @task(4)
    def view_product(self):
        if self.products_ids:
            product_id = random.choice(self.products_ids)
            self.client.get(f"/api/products/{product_id}", name="/api/products/:id")
        else:
            print("No products IDs found")

    @task(3)
    def search_products(self):
        search_term = random.choice(["electronics", "clothing", "laptop", "phone"])
        self.client.get(f"/api/products?search={search_term}", name="/api/products?search")

    @task(3)
    def filter_products_by_category(self):
        if self.categories_ids:
            category_id = random.choice(self.categories_ids)
            self.client.get(f"/api/products?category={category_id}", name="/api/products?category")
        else:
            print("No category IDs found")

    @task(3)
    def filter_products_by_subcategory(self):
        if self.subcategories_ids:
            subcategory_id = random.choice(self.subcategories_ids)
            self.client.get(f"/api/products?subcategory={subcategory_id}", name="/api/products?subcategory")
        else:
            print("No subcategory IDs found")

    @task(2)
    def view_paginated_products(self):
        page = random.randint(1, 10)  # Adjust range based on your pagination setup
        self.client.get(f"/api/products?page={page}", name="/api/products?page")

    @task(2)
    def add_product(self):
        data = {
                "name": fake.word(),
                "description": "n",
                "price": 123,
                "stock_quantity": 1,
                "subcategory": random.choice(self.subcategories_ids)
            }

        # try:
        #     response = self.client.post("/api/products", 
        #                     json=data, 
        #                     name="/api/products (add product)",
        #                     auth=self.auth, 
        #                     headers=self.headers)
        #     # pprint(response.json())
        #     print(f"Response status code: {response.status_code}")
        #     print(f"Response Text: {response.text}")
        # except Exception as e:
        #     pprint(f"Error:  {e}")

        response = self.client.post("/api/products", 
                            json=data, 
                            name="/api/products (add product)",
                            auth=self.auth, 
                            headers=self.headers)
            # pprint(response.json())
        print(f"Response status code: {response.status_code}")
        # print(f"Response Text: {response.text}")
        
        

    @task(3)
    def add_product_to_cart(self):
        if self.products_ids:
            product_id = random.choice(self.products_ids)
            data = {
                "product_id": product_id, 
                "quantity": random.randint(1, 5)}
            try:
                response = self.client.post("/api/cart/items", 
                                json=data, 
                                name="/api/cart/items (add product)",
                                headers=self.headers,
                                auth=self.auth)
                pprint(response.json())
            except Exception as e:
                pprint(e)
        else:
            print("No product IDs found")


    # @task(2)
    # def remove_product_from_cart(self):
    #     if self.products_ids:
    #         product_id = random.choice(self.products_ids)
    #         self.client.delete(f"/api/cart/items/{product_id}", name="/api/cart/:id (remove product)")
    #     else:
    #         print("No product IDs found")

    # @task(2)
    # def update_product_quantity_in_cart(self):
    #     if self.products_ids:
    #         product_id = random.choice(self.products_ids)
    #         data = {"quantity": random.randint(1, 10)}
    #         self.client.put(f"/api/cart/items/{self.cart_id}", json=data, name="/api/cart/:id (update quantity)")
    #     else:
    #         print("No product IDs found")

    @task(3)
    def sort_products(self):
        sort_option = random.choice(["price", "-price", "updated_at", "-updated_at"])
        self.client.get(f"/api/products?ordering={sort_option}", name="/api/products?ordering")
   
    