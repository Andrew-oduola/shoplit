from django.urls import path
from .views import InitializePaymentView, VerifyPaymentView

urlpatterns = [
    path('initialize/<uuid:order_id>/', InitializePaymentView.as_view(), name='initialize_payment'),
    path('verify/<str:reference>/', VerifyPaymentView.as_view(), name='verify_payment'),
]
