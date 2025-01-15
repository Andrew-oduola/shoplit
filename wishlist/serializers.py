from rest_framework import serializers

from .models import WishList
from products.models import Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category', 'subcategory']
class WishListSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = WishList
        fields = ('id', 'user', 'products')

