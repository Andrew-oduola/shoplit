from rest_framework.test import APIClient
from rest_framework import status
import pytest
from customuser.models import CustomUser

class TestCreateCategory:
    @pytest.mark.django_db
    def test_if_anomynous_create_category_return_403(self):
        client = APIClient()
        response = client.post('/api/products/categories/', {
            'name': 'Test Category'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN
        # assert response.data['name'] == 'Test Category'
    @pytest.mark.django_db
    def test_if_is_not_admin_return_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post('/api/products/categories/', {
            'name': 'Test Category'
        })

        assert response.status_code == status.HTTP_403_FORBIDDEN
    @pytest.mark.django_db
    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        client.force_authenticate(user=CustomUser(is_staff=True))
        response = client.post('/api/products/categories/', {'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    @pytest.mark.django_db
    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        client.force_authenticate(user=CustomUser(is_staff=True))
        response = client.post('/api/products/categories/', {'name': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
