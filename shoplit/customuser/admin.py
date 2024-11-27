from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm 

from .models import CustomUser, Vendor


@admin.decorators.register(CustomUser)
class CustomUserAdmin(UserAdmin):
   
    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('email', "is_staff", "last_login", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ('email', )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name"),
            "classes": ("collapse",),
        }),
        ("Permission", {
            "classes": ("collapse",),
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "classes" : ("collapse", ),
            "fields": ("last_login", "date_joined")
        })
    )
    add_fieldsets = (
        (None, 
         {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )