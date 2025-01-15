from rest_framework.routers import DefaultRouter
from .views import WishListViewSet

router = DefaultRouter()

router.register(r'', WishListViewSet, basename='wishlist')

urlpatterns = router.urls
