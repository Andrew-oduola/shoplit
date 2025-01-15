from django.db import models
import uuid

class WishList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        'customuser.CustomUser',
        on_delete=models.CASCADE,
        related_name='wish_list'
    )
    products = models.ManyToManyField(
        'products.Product',
        related_name='wish_lists'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s wishlist"
