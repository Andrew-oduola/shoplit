from django.shortcuts import render

from rest_framework import generics

from .models import CustomUser

from.serializers import RegisterUserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer