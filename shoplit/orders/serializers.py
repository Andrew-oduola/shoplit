from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        # Check stock quantity
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Insufficient stock for product '{product.name}'. Only {product.stock_quantity} available."
            )
        return attrs

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']

        # Check and deduct stock
        if product.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Not enough stock for product {product.name}."
            )

        # Deduct stock quantity
        product.stock_quantity -= quantity
        product.save()

        # Calculate the price based on the product's price and quantity
        price = product.price * quantity
        validated_data['price'] = price  # Set the calculated price

        # Create and return the OrderItem instance
        return super().create(validated_data)

class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        # Extract items data from the validated data
        items_data = validated_data.pop('items')
        
        # Create the order instance
        order = Order.objects.create(**validated_data)

        # Iterate through each item data and create an associated OrderItem instance
        for item_data in items_data:
            # Set the 'order' field for each item to the created order instance
            item_data['order'] = order  # Link the order to the OrderItem
            OrderItemSerializer.create(OrderItemSerializer(), validated_data=item_data)

        return order
    
    def update(self, instance, validated_data):
        # Update the order fields first
        items_data = validated_data.pop('items', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Add new items if provided
        if items_data:
            for item_data in items_data:
                # Link the order to the new item
                item_data['order'] = instance
                OrderItemSerializer.create(OrderItemSerializer(), validated_data=item_data)

        return instance
