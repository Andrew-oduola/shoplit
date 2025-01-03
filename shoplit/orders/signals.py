from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from notifications.models import Notifications

@receiver(post_save, sender=Order)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notifications.objects.create(
            title='New Order',
            message=f'Order {instance.id} has been created',
            user=instance.user
            )

# @receiver(post_save, sender=Order)
# def save_notification(sender, instance, **kwargs):
#     instance.notifications.save()
