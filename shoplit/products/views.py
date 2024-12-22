from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
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
    
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        subcategory_id = self.request.query_params.get('subcategory_id')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        elif subcategory_id:
            queryset = queryset.filter(subcategory__id=subcategory_id)
        return queryset


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

