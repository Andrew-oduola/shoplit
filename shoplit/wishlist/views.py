from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import WishListSerializer
from .models import WishList
# Create your views here.
class WishListViewSet(viewsets.ModelViewSet):
    """
    Handles the WishList Model

    Endpoints
    GET /wishlists/ -> List all the product in the wishlists of a user and all users if user is superuser
    POST /wishlists/ -> Create a new wishlist for a user
    PUT /wishlists/{id} -> Update a wishlist
    DELETE /wishlists/{id} -> Delete a wishlist

    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user)
