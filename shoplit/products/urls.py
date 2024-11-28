from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register(r'Categories', views.CategoryViewSet, basename='categories')
router.register(r'Subcategories', views.SubCategoryViewSet, basename='subcategories')
router.register(r'Products', views.ProductViewSet, basename='products')

urlpatterns = router.urls
