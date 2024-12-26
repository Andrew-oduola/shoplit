from rest_framework.test import APIClient
from rest_framework import status
import pytest
from customuser.models import CustomUser

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


class TestCreateCategory:
    @pytest.mark.django_db
    def test_if_anomynous_create_category_return_403(self, create_category):
        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    @pytest.mark.django_db
    def test_if_is_not_admin_return_403(self, authenticate, create_category):
        authenticate()

        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN


    @pytest.mark.django_db
    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        authenticate(True)

        response = create_category({'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None


    @pytest.mark.django_db
    def test_if_data_is_valid_returns_201(self, authenticate, create_category):
        authenticate(True)

        response = create_category({'name': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None
