# utils.py
from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"SID: {message.sid}")
        return message.sid  # Message SID for reference
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return None
