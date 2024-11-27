from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)

    # The field to use inplace of username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor')
    store_name = models.CharField(_("Vendor Name"), max_length=255)
    store_description = models.TextField(_("Store Description"), blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to="Vendor_logos.", blank=True, null=True)
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=15, blank=True, null=True)
    joined_at  = models.DateTimeField(_("Joined At"), auto_now_add=True)
    is_approved = models.BooleanField(_("Is Approved"), default=False)

    def __str__(self):
        return self.store_name
    

