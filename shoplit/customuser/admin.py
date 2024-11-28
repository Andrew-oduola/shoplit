from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm 

from .models import CustomUser, Vendor


@admin.decorators.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = CustomUser

    list_display = ('email', "is_staff", "last_login", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ('email', )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "image"),
        }),
        ("Permission", {
            "classes": ("collapse",),
            "fields": ("is_active", 
                       "is_staff", 
                       "is_superuser", 
                       "groups", 
                       "user_permissions")
        }),
        ("Important Dates", {
            "classes" : ("collapse", ),
            "fields": ("last_login", 
                       "date_joined")
        })
    )
    add_fieldsets = (
        (None, 
         {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'phone', 'joined_at')
    search_fields = ('user', 'store_name', 'user__email')
    ordering = ('store_name', 'user')
    fieldsets = (
        ("Store Info", {'fields': ('store_name', 
                                   'user', 
                                   'store_description',
                                   'logo')}),
                        
        ("Contact", {
            'fields': ('phone', 
                       'address')}),
        ("More Info", {
            'fields': ('is_approved',)
        })
    )
