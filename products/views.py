from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import APIException, ValidationError

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import CategorySerializer, SubCategorySerializer, \
    ProductSerializer, ProductCreateUpdateSerializer
from .permissions import IsAdminUserOrReadOnly
from .models import Category, SubCategory, Product
from .filters import ProductFilterSet

from drf_spectacular.utils import extend_schema, extend_schema_view

import logging

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="List categories", tags=["Category"]),
    retrieve=extend_schema(summary="Retrieve a category", tags=["Category"]),
    create=extend_schema(summary="Create category", tags=["Category"]),
    update=extend_schema(summary="Update category", tags=["Category"]),
    partial_update=extend_schema(summary="Partially update category", tags=["Category"]),
    destroy=extend_schema(summary="Delete category", tags=["Category"]),
)
class CategoryViewSet(ModelViewSet):
   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'updated_at']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        logger.info("User %s requested category list.", request.user)
        try:
            response = super().list(request, *args, **kwargs)
            logger.debug("List response: %s", response.data)
            return response
        except Exception as e:
            logger.error("Unexpected error in list view: %s", str(e), exc_info=True)
            raise APIException("An error occurred while fetching the category list.")

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        logger.info("User %s requested category details for ID %s.", request.user, category_id)
        try:
            response = super().retrieve(request, *args, **kwargs)
            logger.debug("Retrieve response for ID %s: %s", category_id, response.data)
            return response
        except ObjectDoesNotExist:
            logger.warning("Category with ID %s does not exist.", category_id)
            raise APIException(f"Category with ID {category_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while retrieving category ID %s: %s", category_id, str(e), exc_info=True)
            raise APIException("An error occurred while retrieving the category.")


    def create(self, request, *args, **kwargs):
        logger.info("User %s is creating a new category.", request.user)
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("Category created successfully. ID: %s", response.data.get('id'))
            return response
        except ValidationError as ve:
            logger.warning("Validation error during category creation: %s", ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during category creation: %s", str(e), exc_info=True)
            raise APIException("An error occurred while creating the category.")


    def update(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        logger.info("User %s is updating category ID %s.", request.user, category_id)
        try:
            response = super().update(request, *args, **kwargs)
            logger.info("Category ID %s updated successfully.", category_id)
            return response
        except ValidationError as ve:
            logger.warning("Validation error during update for category ID %s: %s", category_id, ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during update for category ID %s: %s", category_id, str(e), exc_info=True)
            raise APIException("An error occurred while updating the category.")


    def destroy(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        logger.warning("User %s is deleting category ID %s.", request.user, category_id)
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("Category ID %s deleted successfully.", category_id)
            return response
        except ObjectDoesNotExist:
            logger.warning("Category ID %s not found for deletion.", category_id)
            raise APIException(f"Category with ID {category_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while deleting category ID %s: %s", category_id, str(e), exc_info=True)
            raise APIException("An error occurred while deleting the category.")


@extend_schema_view(
    list=extend_schema(summary="List subcategories", tags=["SubCategory"]),
    retrieve=extend_schema(summary="Retrieve a subcategory", tags=["SubCategory"]),
    create=extend_schema(summary="Create subcategory", tags=["SubCategory"]),
    update=extend_schema(summary="Update subcategory", tags=["SubCategory"]),
    partial_update=extend_schema(summary="Partially update subcategory", tags=["SubCategory"]),
    destroy=extend_schema(summary="Delete subcategory", tags=["SubCategory"]),
)
class SubCategoryViewSet(ModelViewSet):
    """
    Handles operations for SubCategory model.

    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name','description']
    ordering_fields = ['name', 'updated_at']
    filterset_fields = ['category']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        logger.info("User %s requested subcategory list.", request.user)
        try:
            response = super().list(request, *args, **kwargs)
            logger.debug("List response: %s", response.data)
            return response
        except Exception as e:
            logger.error("Unexpected error in list view: %s", str(e), exc_info=True)
            raise APIException("An error occurred while fetching the subcategory list.")

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        subcategory_id = kwargs.get('pk')
        logger.info("User %s requested subcategory details for ID %s.", request.user, subcategory_id)
        try:
            response = super().retrieve(request, *args, **kwargs)
            logger.debug("Retrieve response for ID %s: %s", subcategory_id, response.data)
            return response
        except ObjectDoesNotExist:
            logger.warning("SubCategory with ID %s does not exist.", subcategory_id)
            raise APIException(f"SubCategory with ID {subcategory_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while retrieving subcategory ID %s: %s", subcategory_id, str(e), exc_info=True)
            raise APIException("An error occurred while retrieving the subcategory.")

    def create(self, request, *args, **kwargs):
        logger.info("User %s is creating a new subcategory.", request.user)
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("SubCategory created successfully. ID: %s", response.data.get('id'))
            return response
        except ValidationError as ve:
            logger.warning("Validation error during subcategory creation: %s", ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during subcategory creation: %s", str(e), exc_info=True)
            raise APIException("An error occurred while creating the subcategory.")

    def update(self, request, *args, **kwargs):
        subcategory_id = kwargs.get('pk')
        logger.info("User %s is updating subcategory ID %s.", request.user, subcategory_id)
        try:
            response = super().update(request, *args, **kwargs)
            logger.info("SubCategory ID %s updated successfully.", subcategory_id)
            return response
        except ValidationError as ve:
            logger.warning("Validation error during update for subcategory ID %s: %s", subcategory_id, ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during update for subcategory ID %s: %s", subcategory_id, str(e), exc_info=True)
            raise APIException("An error occurred while updating the subcategory.")

    def destroy(self, request, *args, **kwargs):
        subcategory_id = kwargs.get('pk')
        logger.warning("User %s is deleting subcategory ID %s.", request.user, subcategory_id)
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("SubCategory ID %s deleted successfully.", subcategory_id)
            return response
        except ObjectDoesNotExist:
            logger.warning("SubCategory ID %s not found for deletion.", subcategory_id)
            raise APIException(f"SubCategory with ID {subcategory_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while deleting subcategory ID %s: %s", subcategory_id, str(e), exc_info=True)
            raise APIException("An error occurred while deleting the subcategory.")


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(summary="List products", tags=["Product"]),
    retrieve=extend_schema(summary="Retrieve a product", tags=["Product"]),
    create=extend_schema(summary="Create product", tags=["Product"]),
    update=extend_schema(summary="Update product", tags=["Product"]),
    partial_update=extend_schema(summary="Partially update product", tags=["Product"]),
    destroy=extend_schema(summary="Delete product", tags=["Product"]),
)
class ProductViewSet(ModelViewSet):
    """
    Handles operations for Product model.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_serializer_class(self):
        """
        Returns a different serializer for the 'create' action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer  # Serializer for creating a product
        return super().get_serializer_class()

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        logger.info("User %s requested product list.", request.user)
        try:
            response = super().list(request, *args, **kwargs)
            logger.debug("List response: %s", response.data)
            return response
        except Exception as e:
            logger.error("Unexpected error in list view: %s", str(e), exc_info=True)
            raise APIException("An error occurred while fetching the product list.")

    @method_decorator(cache_page(60 * 10))
    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        logger.info("User %s requested product details for ID %s.", request.user, product_id)
        try:
            response = super().retrieve(request, *args, **kwargs)
            logger.debug("Retrieve response for ID %s: %s", product_id, response.data)
            return response
        except ObjectDoesNotExist:
            logger.warning("Product with ID %s does not exist.", product_id)
            raise APIException(f"Product with ID {product_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while retrieving product ID %s: %s", product_id, str(e), exc_info=True)
            raise APIException("An error occurred while retrieving the product.")

    def create(self, request, *args, **kwargs):
        logger.info("User %s is creating a new product.", request.user)
        try:
            response = super().create(request, *args, **kwargs)
            logger.info("Product created successfully. ID: %s", response.data.get('id'))
            return response
        except ValidationError as ve:
            logger.warning("Validation error during product creation: %s", ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during product creation: %s", str(e), exc_info=True)
            raise APIException("An error occurred while creating the product.")

    def update(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        logger.info("User %s is updating product ID %s.", request.user, product_id)
        try:
            response = super().update(request, *args, **kwargs)
            logger.info("Product ID %s updated successfully.", product_id)
            return response
        except ValidationError as ve:
            logger.warning("Validation error during update for product ID %s: %s", product_id, ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error during update for product ID %s: %s", product_id, str(e), exc_info=True)
            raise APIException("An error occurred while updating the product.")

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs.get('pk')
        logger.warning("User %s is deleting product ID %s.", request.user, product_id)
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info("Product ID %s deleted successfully.", product_id)
            return response
        except ObjectDoesNotExist:
            logger.warning("Product ID %s not found for deletion.", product_id)
            raise APIException(f"Product with ID {product_id} not found.")
        except Exception as e:
            logger.error("Unexpected error while deleting product ID %s: %s", product_id, str(e), exc_info=True)
            raise APIException("An error occurred while deleting the product.")

  
