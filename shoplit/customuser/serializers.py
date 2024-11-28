from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from .models import CustomUser, Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'store_description', 'address', 'logo', 'phone', 'is_approved', 'joined_at']

class UserSerializer(BaseUserSerializer, serializers.HyperlinkedModelSerializer):
    vendor = VendorSerializer(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'vendor']

class UserCreateSerializer(BaseUserCreateSerializer, serializers.HyperlinkedModelSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


