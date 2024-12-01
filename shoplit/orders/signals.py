from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def notify_user_order_status(sender, instance, **kwargs):
    if instance.status == 'DELIVERED':
        # Send email notification to user
        print(f"Order {instance.id} has been delivered to {instance.user.email}.")

