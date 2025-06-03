"""
URL configuration for shoplit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path('', lambda request: redirect('swagger-ui', permanent=False)),  # Add this line
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('djoser.urls')),  # User registration and profile management
    re_path(r'^auth/', include('djoser.urls.jwt')),  # JWT authentication
    path('api/', include('customuser.urls')),  # Custom user-related actions
    path('api/products/', include('products.urls')),  # Product and category management
    path('api/cart/', include('carts.urls')),  # Shopping cart management
    path('api/orders/', include('orders.urls')), # Orders management
    path('api/wishlist/', include('wishlist.urls')), # Wishlist management
    path('api/payments/', include('payments.urls')), # Payments management
    path('api/reviews/', include('reviews.urls')), # Reviews management
    path('api/notifications/', include('notifications.urls')), # Notifications management
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Add debug toolbar URLs in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
