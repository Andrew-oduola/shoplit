from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'ref', 'amount', 'created_at']
        read_only_fields = ['ref', 'created_at']
