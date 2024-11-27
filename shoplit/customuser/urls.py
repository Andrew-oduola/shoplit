from rest_framework.routers import DefaultRouter
from .views import RegisterView

from django.urls import path


# router = DefaultRouter()
# router.register(r'users', RegisterView, basename='user')

urlpatterns = (
    path('register/', RegisterView.as_view(), name='register'),
)