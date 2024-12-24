from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, SubCategorySerializer, \
    ProductSerializer
from rest_framework.permissions import IsAdminOrReadOnly
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
    permission_classes = [IsAdminOrReadOnly]

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
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']

  


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product

class AdjustStockView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            quantity = int(request.data.get('quantity'))
            adjustment_type = request.data.get('type', 'MANUAL').upper()

            if adjustment_type == 'INCREASE':
                product.increase_stock(quantity)
            elif adjustment_type == 'DECREASE':
                product.reduce_stock(quantity)
            else:
                return Response({"error": "Invalid adjustment type"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Stock updated successfully"}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

