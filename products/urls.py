from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Initialize the router and register viewsets for categories, subcategories, and products
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'subcategories', views.SubCategoryViewSet, basename='subcategories')
router.register(r'', views.ProductViewSet, basename='products')

# Use the router-generated URLs
urlpatterns = router.urls
