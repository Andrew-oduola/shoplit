from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from notifications.models import Notifications
from django_q.tasks import async_task

@receiver(post_save, sender=Order)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Trigger an async task for in-app notification
        async_task("orders.tasks.send_order_notification", instance.user.id, instance.id)

        async_task(
            "notifications.twilio.send_sms_notification",
            instance.user.phone_number,
            f"Your order {instance.id} has been created successfully!",
        )


# @receiver(post_save, sender=Order)
# def save_notification(sender, instance, **kwargs):
#     instance.notifications.save()
