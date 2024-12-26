from rest_framework.test import APIClient
from rest_framework import status

import pytest
from model_bakery import baker

from customuser.models import CustomUser
from products.models import Category, SubCategory, Product

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=CustomUser(is_staff=is_staff)) 
    return do_authenticate

@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post('/api/products/categories/', category)
    return do_create_category

@pytest.mark.django_db
class TestCreateCategory:
    
    def test_if_anomynous_create_category_return_403(self, create_category):
        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    
    def test_if_is_not_admin_return_403(self, authenticate, create_category):
        authenticate()

        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    
    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        authenticate(True)

        response = create_category({'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None


    
    def test_if_data_is_valid_returns_201(self, authenticate, create_category):
        authenticate(True)

        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None
@pytest.mark.django_db
class TestRetrieveCategory:
    def test_if_category_exist_returns_200(self, api_client):
        category = baker.make(Category)

        response = api_client.get(f'/api/products/categories/{category.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_category_did_not_exist_returns_404(self, api_client):
        response = api_client.get(f'/api/products/categories/wwwwwwwwwwww4ew/')

        assert response.status_code == status.HTTP_404_NOT_FOUND