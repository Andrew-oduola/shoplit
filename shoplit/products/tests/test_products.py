from rest_framework import status

from products.models import Product, Category, SubCategory
from customuser.models import CustomUser

import pytest
from model_bakery import baker

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=CustomUser(is_staff=is_staff))
    return do_authenticate

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('api/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestListProducts:
    def test_if_list_products_returns_200(self, api_client):
        response = api_client.get('/api/products/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_list_products_returns_empty_list(self, api_client):
        response = api_client.get('/api/products/')

        assert response.data['count'] == 0

    def test_if_list_products_returns_list(self, api_client):
        subcategory = baker.make(Product)   

        response = api_client.get('/api/products/')

        assert response.data['count'] > 0

    def test_if_list_products__category_returns_filtered_list(self, api_client):
        category = baker.make(Category)
        product = baker.make(Product, category=category)   
        response = api_client.get(f'/api/products/?category={product.category.id}')

        assert response.data['count'] > 0


    def test_if_list_products__subcategory_returns_filtered_list(self, api_client):
        category = baker.make(Category)
        subcategory = baker.make(SubCategory, category=category)
        product = baker.make(Product, subcategory=subcategory, category=category)   
        response = api_client.get(f'/api/products/?subcategory={product.subcategory.id}')

        assert response.data['count'] > 0


    def test_if_list_products_price_equals_returns_filtered_list(self, api_client):
        product = baker.make(Product, price=100)   
        response = api_client.get(f'/api/products/?price={product.price}')

        assert response.data['count'] > 0


    def test_if_list_products_price_gte_returns_filtered_list(self, api_client):
        product = baker.make(Product, price=100)  
        response = api_client.get(f'/api/products/?price__gte={product.price}')

        assert response.data['count'] > 0


    def test_if_list_products_price_lte_returns_filtered_list(self, api_client):
        product = baker.make(Product, price=100)   
        response = api_client.get(f'/api/products/?price__lte={product.price}')

        assert response.data['count'] > 0


    def test_if_list_products_price_lte_and_gte_returns_filtered_list(self, api_client):
        product = baker.make(Product, price=100)
        product2 = baker.make(Product, price=200)   
        response = api_client.get(f'/api/products/?price__lte={product2.price}&price__gte={product.price}')

        assert response.data['count'] > 0


    def test_if_list_products_name_contains_returns_filtered_list(self, api_client):
        product = baker.make(Product, name="name")  
        response = api_client.get(f'/api/products/?name={product.name}')

        assert response.data['count'] > 0


    def test_if_list_products_description_contains_returns_filtered_list(self, api_client):
        product = baker.make(Product, description="description")
        response = api_client.get(f'/api/products/?description__icontains={product.description}')

        assert response.data['count'] > 0


    def test_if_list_products_returns_search_list(self, api_client):
        product = baker.make(Product, name="name")   
        response = api_client.get(f'/api/products/?search={product.name[:3]}')

        assert response.data['count'] > 0

    def test_if_list_products_returns_price_accending_ordered_list(self, api_client):
        product = baker.make(Product, name="name")   
        response = api_client.get(f'/api/products/?ordering=price')

        assert response.data['count'] > 0

    def test_if_list_products_returns_price_descending_ordered_list(self, api_client):
        product = baker.make(Product, name="name")   
        response = api_client.get(f'/api/products/?ordering=-price')

        assert response.data['count'] > 0

    def test_if_list_products_returns_updated_at_accending_ordered_list(self, api_client):
        product = baker.make(Product, name="name")   
        response = api_client.get(f'/api/products/?ordering=updated_at')

        assert response.data['count'] > 0

    
    def test_if_list_products_returns_updated_at_descending_ordered_list(self, api_client):
        product = baker.make(Product, name="name")   
        response = api_client.get(f'/api/products/?ordering=-updated_at')

        assert response.data['count'] > 0

    def test_if_bad_filtered_products_returns_400(self, api_client):
        response = api_client.get(f'/api/products/?category_id=1')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


    
    