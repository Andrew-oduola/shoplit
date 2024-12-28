from rest_framework import status

from products.models import Product, Category, SubCategory
from customuser.models import CustomUser

import pytest
from model_bakery import baker
from decimal import Decimal

@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=CustomUser(is_staff=is_staff))
    return do_authenticate

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/api/products/', product)
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

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_anomynous_create_product_return_403(self, create_product):
        subcategory = baker.make(SubCategory)
        response = create_product(
            {
                "name": "n",
                "description": "n",
                "price": 123,
                "stock_quantity": 1,
                "subcategory": subcategory.id
            }
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_is_not_admin_return_403(self, authenticate, create_product):
        authenticate()

        response = create_product({'name': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(True)

        response = create_product({'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None


    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)
        subcategory = baker.make(SubCategory)
        response = create_product(
            {
                "name": "n",
                "description": "n",
                "price": 123,
                "stock_quantity": 1,
                "subcategory": subcategory.id
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] is not None

    def test_if_product_created_with_valid_data_returns_expected_data(self, authenticate, create_product):
        authenticate(is_staff=True)
        subcategory = baker.make(SubCategory)
        response = create_product(
            {
                "name": "n",
                "description": "n",
                "price": 123,
                "stock_quantity": 1,
                "subcategory": subcategory.id
            }
        )

        assert response.data['name'] == 'n'
        assert response.data['description'] == 'n'
        assert response.data['price'] == 123
        assert response.data['stock_quantity'] == 1
        # assert response.data['subcategory']['id'] == subcategory.id

@pytest.mark.django_db
class TestRetriveProduct:
    def test_if_product_exist_returns_200(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/api/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK

    def test_if_product_does_not_exist_returns_404(self, api_client):
        response = api_client.get(f'/api/products/1/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_product_exist_returns_expected_data(self, api_client):
        product = baker.make(Product)
        response = api_client.get(f'/api/products/{product.id}/')

        assert response.data['name'] == product.name
        assert response.data['description'] == product.description
        assert response.data['price'] == Decimal(product.price)
        assert response.data['stock_quantity'] == product.stock_quantity
        # assert response.data['subcategory']['id'] == product.subcategory.id

@pytest.mark.django_db
class TestUpdateProduct:
    def test_update_put_product_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)
        category = baker.make(Category)
        subcategory = baker.make(SubCategory)
        data = {}
        response = api_client.put(f'/api/products/{product.id}/', 
        {
            "id": "0ebd1c22-4bab-4ee3-a329-977688260951",
            "name": "free",
            "description": "Why information gun make toward law us day. Education give guess state may six.\nStreet letter executive difference. Out some compare beyond note piece past town.",
            "price": 812.94,
            "stock_quantity": 8,
            "category": category.id,
            "subcategory": subcategory.id,
            "average_rating": 0.0,
            "review_count": 0.0
        })

        assert response.status_code == status.HTTP_200_OK

    def test_if_update_put_product_returns_403_for_non_staff(self, authenticate, api_client):
        authenticate()
        product = baker.make(Product)

        response = api_client.put(f'/api/products/{product.id}/', {'name': 'update', 'description': 'desc', 'price': 123, 'stock_quantity': 1})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_update_put_product_returns_400_for_invalid_data(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.put(f'/api/products/{product.id}/', {'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_update_put_product_returns_expected_data(self, authenticate, api_client):
        authenticate(is_staff=True)
        category = baker.make(Category)
        subcategory = baker.make(SubCategory, category=category)
        product = baker.make(Product, category=category, subcategory=subcategory)
        
        data = {
            "id": str(product.id),
            "name": "free",
            "description": "Why",
            "price": "812.94",
            "stock_quantity": 8,
            "category": category.name,
            "subcategory": str(subcategory.id),
            "average_rating": 0.0,
            "review_count": 0.0
        }
        response = api_client.put(f'/api/products/{product.id}/', data)

        assert response.data['name'] == 'free'
        assert response.data['description'] == 'Why'
        assert response.data['price'] == Decimal("812.94")
        assert response.data['stock_quantity'] == 8

    def test_if_update_patch_product_returns_200(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.patch(f'/api/products/{product.id}/', {'name': 'update'})

        assert response.status_code == status.HTTP_200_OK

    def test_if_update_patch_product_returns_403_for_non_staff(self, authenticate, api_client):
        authenticate()
        product = baker.make(Product)

        response = api_client.patch(f'/api/products/{product.id}/', {'name': 'update'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_update_patch_product_returns_400_for_invalid_data(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.patch(f'/api/products/{product.id}/', {'name': ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_update_patch_product_returns_expected_data(self, authenticate, api_client):
        authenticate(is_staff=True)
        product = baker.make(Product)

        response = api_client.patch(f'/api/products/{product.id}/', {'name': 'update'})
        assert response.data['name'] == 'update'



