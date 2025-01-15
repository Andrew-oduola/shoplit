from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.CartItemViewSet, basename='cart-item')
router.register(r'', views.CartViewSet, basename='cart')

urlpatterns = router.urls
