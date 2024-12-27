from rest_framework import status

import pytest
from model_bakery import baker

from customuser.models import CustomUser
from products.models import Category, SubCategory


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=CustomUser(is_staff=is_staff)) 
    return do_authenticate


@pytest.fixture
def create_subcategory(api_client):
    def do_create_subcategory(subcategory):
        return api_client.post('/api/products/subcategories/', subcategory)
    return do_create_subcategory


@pytest.mark.django_db
class TestListSubCategories:
    def test_if_list_subcategories_returns_200(self, api_client):
        response = api_client.get('/api/products/subcategories/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_empty_list(self, api_client):
        response = api_client.get('/api/products/subcategories/')

        assert response.data['count'] == 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_list(self, api_client):
        subcategory = baker.make(SubCategory)   

        response = api_client.get('/api/products/subcategories/')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_filtered_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?category={subcategory.category.id}')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_searched_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?search={subcategory.name}')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_name_assending_ordered_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?ordering=name')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_name_descending_ordered_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?ordering=-name')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_list_subcategories_returns_update_at_assending_ordered_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?ordering=update_at')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK


    def test_if_list_subcategories_returns_update_at_descending_ordered_list(self, api_client):
        subcategory = baker.make(SubCategory)   
        response = api_client.get(f'/api/products/subcategories/?ordering=-update_at')

        assert response.data['count'] > 0
        assert response.status_code == status.HTTP_200_OK

    def test_if_bad_filtered_subcategories_returns_400(self, api_client):
        response = api_client.get(f'/api/products/subcategories/?category=1') 
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    
@pytest.mark.django_db
class TestCreateSubCategory:
    
    def test_if_anomynous_create_subcategory_return_403(self, create_subcategory):
        category = baker.make(Category)
        response = create_subcategory({"name": "n", "description": "n", "category": category.id})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    
    def test_if_is_not_admin_create_subcategory_return_403(self, authenticate, create_subcategory):
        authenticate()
        category = baker.make(Category)

        response = create_subcategory({'name': 'a', "description": "n", "category": category.id})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    
    def test_if_data_is_invalid_create_subcategory_returns_400(self, authenticate, create_subcategory):
        authenticate(True)

        response = create_subcategory({'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None


    def test_if_create_subcategory_data_is_valid_returns_201(self, authenticate, create_subcategory):
        authenticate(is_staff=True)
        category = baker.make(Category)

        response = create_subcategory({'name': 'a', "description": "n", "category": category.id})


        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None

    def test_if_subcategoy_created_with_valid_data_return_expected_data(self,authenticate, create_subcategory):
        authenticate(is_staff=True)
        category = baker.make(Category)
        response = create_subcategory(
            {
                'name': 'name', 
                'description': 'desc', 
                'category': category.id
            }
        ) 

        assert response.data['name'] == 'name'
        # assert response.description == 'desc'
        # assert response.category == category

@pytest.mark.django_db
class TestRetrieveSubCategory:
    def test_if_subcategory_exist_returns_200(self, api_client):
        subcategory = baker.make(SubCategory)

        response = api_client.get(f'/api/products/subcategories/{subcategory.id}/')

        assert response.status_code == status.HTTP_200_OK


    def test_if_subcategory_did_not_exist_returns_404(self, api_client):
        response = api_client.get(f'/api/products/subcategories/wwwwwwwwwwww4ew/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    
    def test_if_subcategory_exist_returns_expected_data(self, api_client):
        subcategory = baker.make(SubCategory)

        response = api_client.get(f'/api/products/subcategories/{subcategory.id}/')

        assert response.data['name'] == subcategory.name
        assert response.data['description'] == subcategory.description
        assert response.data['category'] == subcategory.category.id

@pytest.mark.django_db
class TestUpdateSubCategory:
    def test_update_put_subcategory_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        subcategory = baker.make(SubCategory)

        response = api_client.put(f'/api/products/subcategories/{subcategory.id}/', {'name': 'n', 'description': 'Description', 'category': subcategory.category.id})

        assert response.status_code == status.HTTP_200_OK     


    def test_if_update_subcategory_returns_403_for_non_staff(self, authenticate, api_client):
        authenticate()
        subcategory = baker.make(SubCategory)

        response = api_client.put(f'/api/products/subcategories/{subcategory.id}/', {'name': 'update', 'description': 'desc', 'category': subcategory.category.id})
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    

@pytest.mark.django_db
class TestDeleteSubCategory:
    def test_if_delete_category_returns_204(self, api_client, authenticate):
        authenticate(is_staff=True)
        subcategory = baker.make(SubCategory)

        response = api_client.delete(f'/api/products/subcategories/{subcategory.id}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT  


    def test_if_delete_category_returns_403_for_non_staff(self, api_client, authenticate):
        authenticate()
        subcategory = baker.make(SubCategory)

        response = api_client.delete(f'/api/products/subcategories/{subcategory.id}/')

        assert response.status_code == status.HTTP_403_FORBIDDEN

        