from rest_framework.routers import DefaultRouter
from .views import VendorViewset

from django.urls import path


router = DefaultRouter()
router.register(r'vendors', VendorViewset, basename='vendors')

urlpatterns = router.urls 