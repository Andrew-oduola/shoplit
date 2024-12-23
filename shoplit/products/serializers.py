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
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.FloatField(read_only=True)
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock_quantity',
            'category',  # Auto-populated based on the subcategory
            'subcategory',
            'average_rating',
            'review_count'
        ]
        read_only_fields = ['category']

    def create(self, validated_data):
        """
        Automatically sets the category based on the subcategory during product creation.
        """
        subcategory = validated_data.get('subcategory')
        if not subcategory or not subcategory.category:
            raise serializers.ValidationError(
                "Invalid subcategory: ensure it is linked to a category."
            )

        validated_data['category'] = subcategory.category
        return super().create(validated_data)
