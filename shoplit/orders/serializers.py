from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    # price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Insufficient stock for product '{product.name}'. Only {product.stock_quantity} available."
            )
        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']

        # Deduct stock
        product.stock_quantity -= quantity
        product.save()

        # Calculate the price based on the product's price and quantity
        price = product.price * quantity
        validated_data['price'] = price  # Set the calculated price
        
        return super().create(validated_data)



class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
