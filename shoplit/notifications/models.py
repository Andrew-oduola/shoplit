from django.db import models


# Create your models here.
class Notifications(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title