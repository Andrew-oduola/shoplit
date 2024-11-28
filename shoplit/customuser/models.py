from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager

from phonenumber_field.modelfields import PhoneNumberField


import uuid

# Custom User Model
class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email address"), unique=True)
    image = models.ImageField(_("Profile Picture"), upload_to='users/profile_pictures/', null=True, blank=True)

    # The field to use in place of the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Vendor Model
class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor')
    store_name = models.CharField(_("Store Name"), max_length=255)
    store_description = models.TextField(_("Store Description"), blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to="vendor_logos/", blank=True, null=True)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)  
    joined_at = models.DateTimeField(_("Joined At"), auto_now_add=True)
    is_approved = models.BooleanField(_("Is Approved"), default=False)

    def __str__(self):
        return self.store_name
