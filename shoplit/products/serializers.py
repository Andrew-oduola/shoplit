from rest_framework import serializers

from .models import Category, SubCategory, Product
from carts.models import CartItem, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'category']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category', 'subcategory']
        read_only_fields = ['category']  # Make the category read-only since it's auto-populated

    def create(self, validated_data):
        subcategory = validated_data.get('subcategory')
        if not subcategory or not subcategory.category:
            raise serializers.ValidationError("Invalid subcategory: ensure it is linked to a category.")

        # Automatically set the category based on the subcategory
        validated_data['category'] = subcategory.category

        # Create the Product instance
        return super().create(validated_data)
    
