from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'subcategories', views.SubCategoryViewSet, basename='subcategories')
router.register(r'', views.ProductViewSet, basename='products')


urlpatterns = router.urls
