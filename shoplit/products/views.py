from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer, SubCategorySerializer, \
    ProductSerializer
from .models import Category, SubCategory, Product



class CategoryViewSet(ModelViewSet):
    """
    Handles operations for Category model.

    Endpoints:
        - GET    /categories/        -> List all categories.
        - POST   /categories/        -> Create a new category.
        - GET    /categories/{id}/   -> Retrieve a specific category.
        - PUT    /categories/{id}/   -> Update a specific category.
        - PATCH  /categories/{id}/   -> Partially update a category.
        - DELETE /categories/{id}/   -> Delete a category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(ModelViewSet):
    """
    Handles operations for SubCategory model.

    Endpoints:
        - GET    /subcategories/        -> List all subcategories.
        - POST   /subcategories/        -> Create a new subcategory.
        - GET    /subcategories/{id}/   -> Retrieve a specific subcategory.
        - PUT    /subcategories/{id}/   -> Update a specific subcategory.
        - PATCH  /subcategories/{id}/   -> Partially update a subcategory.
        - DELETE /subcategories/{id}/   -> Delete a subcategory.
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ProductViewSet(ModelViewSet):
    """
    Handles operations for Product model.

    Endpoints:
        - GET    /products/        -> List all products.
        - POST   /products/        -> Create a new product.
        - GET    /products/{id}/   -> Retrieve a specific product.
        - PUT    /products/{id}/   -> Update a specific product.
        - PATCH  /products/{id}/   -> Partially update a product.
        - DELETE /products/{id}/   -> Delete a product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
