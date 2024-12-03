from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import WishListSerializer
from .models import WishList
# Create your views here.
class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user)
