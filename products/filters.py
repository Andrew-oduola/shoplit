from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            'category_id': ['exact'],
            'subcategory_id': ['exact'],
            'price': ['gte', 'lte'],
            'name': ['icontains'],
            'description': ['icontains'],
        }