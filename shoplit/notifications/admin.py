from django.contrib import admin
from .models import Notifications

# Register your models here.
@admin.register(Notifications)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'message', 'created_at', 'updated_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['title', 'message']
    list_editable = ['is_read']
    list_display_links = ['title']
    list_per_page = 10
    list_max_show_all = 100


