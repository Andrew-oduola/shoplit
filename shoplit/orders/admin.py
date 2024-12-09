from django.contrib import admin
from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):  # Use TabularInline for inline editing
    model = OrderItem
    fields = ('product', 'quantity', 'price')  # Specify fields to display inline
    extra = 1  # Number of extra empty fields to show for new items


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at')  # Added updated_at for better tracking
    inlines = [OrderItemInline]  # Add the inline admin for OrderItems


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')  # Display individual OrderItems in their own view
    list_filter = ('product', 'order')  # Optional: Filters for easy navigation
    search_fields = ('order__user__email', 'product__name')  # Optional: Search fields for better usability
