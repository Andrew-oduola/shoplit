from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage
from carts.models import CartItem, Cart


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'category']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)  # Display images
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.FloatField(read_only=True)
    # category = serializers.StringRelatedField()

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
            'review_count',
            'images'
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


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'subcategory', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        product = Product.objects.create(**validated_data)

        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return product
