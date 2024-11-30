from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
router = DefaultRouter()
router.register(r'Categories', views.CategoryViewSet, basename='categories')
router.register(r'Subcategories', views.SubCategoryViewSet, basename='subcategories')
router.register(r'Products', views.ProductViewSet, basename='products')
router.register(r'cart/items', views.CartItemViewSet, basename='cart-item')
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = router.urls
