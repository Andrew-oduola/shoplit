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

        # Iterate through each item data and create/update associated OrderItem instances
        for item_data in items_data:
            product = item_data['product']
            existing_item = OrderItem.objects.filter(order=order, product=product).first()

            if existing_item:
                # Update quantity and price of the existing item
                existing_item.quantity += item_data['quantity']
                if product.stock_quantity < item_data['quantity']:
                    raise serializers.ValidationError(
                        f"Not enough stock for product {product.name}."
                    )
                product.stock_quantity -= item_data['quantity']
                product.save()
                existing_item.price = product.price * existing_item.quantity
                existing_item.save()
            else:
                # Create a new item if it doesn't already exist
                item_data['order'] = order
                OrderItemSerializer.create(OrderItemSerializer(), validated_data=item_data)

        return order

    def update(self, instance, validated_data):
        # Update the order fields
        items_data = validated_data.pop('items', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle items: update existing or add new
        for item_data in items_data:
            product = item_data['product']
            existing_item = OrderItem.objects.filter(order=instance, product=product).first()

            if existing_item:
                # Update quantity and price of the existing item
                existing_item.quantity += item_data['quantity']
                if product.stock_quantity < item_data['quantity']:
                    raise serializers.ValidationError(
                        f"Not enough stock for product {product.name}."
                    )
                product.stock_quantity -= item_data['quantity']
                product.save()
                existing_item.price = product.price * existing_item.quantity
                existing_item.save()
            else:
                # Create a new item if it doesn't already exist
                item_data['order'] = instance
                OrderItemSerializer.create(OrderItemSerializer(), validated_data=item_data)

        return instance
