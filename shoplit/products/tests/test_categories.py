from rest_framework.test import APIClient
from rest_framework import status
import pytest

class TestCreateCategory:
    @pytest.mark.django_db
    def test_if_anomynous_create_category_return_401(self):
        client = APIClient()
        response = client.post('/api/products/categories/', {
            'name': 'Test Category'
        })

        assert response.status_code == status.HTTP_201_CREATED
        # assert response.data['name'] == 'Test Category'