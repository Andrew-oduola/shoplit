from django_q.tasks import async_task
from notifications.models import Notifications
from twilio.rest import Client
from orders.models import Order

def send_order_notification(user_id, order_id):
    # Create an in-app notification
    try:
        # Fetch order details if needed
        order = Order.objects.get(id=order_id)

        # Create the notification
        Notifications.objects.create(
            user_id=user_id,
            title="Order Created",
            message=f"Your order {order.id} has been successfully created. Total amount: ${order.total_amount}.",
        )

        print(f"Notification created for order {order.id} successfully.")
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist.")
    except Exception as e:
        print(f"Failed to create notification for order {order_id}: {e}")



def send_sms_notification(phone_number, message):
    # Use Twilio or another SMS service to send the SMS
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_="your_twilio_phone_number",
        to=phone_number,
    )
