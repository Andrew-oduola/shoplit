from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import CategorySerializer, SubCategorySerializer, \
    ProductSerializer, ProductCreateUpdateSerializer
from .permissions import IsAdminUserOrReadOnly
from .models import Category, SubCategory, Product
from .filters import ProductFilterSet


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
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','description']
    ordering_fields = ['name', 'updated_at']

    # Cache the list view for 5 minutes
    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Cache the retrieve view for 10 minutes
    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    

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
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name','description']
    ordering_fields = ['name', 'updated_at']
    filterset_fields = ['category']

    # Cache the list view for 5 minutes
    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Cache the retrieve view for 10 minutes
    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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
    pagination_class = CustomPagination
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']

    def get_serializer_class(self):
        """
        Returns a different serializer for the 'create' action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer  # Serializer for creating a product
        return super().get_serializer_class()

    # Cache the list view for 5 minutes
    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Cache the retrieve view for 10 minutes
    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

  
