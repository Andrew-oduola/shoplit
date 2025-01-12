import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Payment
from .serializers import PaymentSerializer
from .paystack import Paystack
from orders.models import Order  # Import your Order model
from notifications.models import Notifications
from notifications import twilio

# Configure logger
logger = logging.getLogger(__name__)

class InitializePaymentView(APIView):
    """ 
    Initialize payment for an order.

    Endpoint: 
    POST /payments/initialize/{order_id} -> Initialize Payment
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            logger.info(f"Order {order_id} found for user {request.user.username}.")
        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found for user {request.user.username}.")
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        paystack = Paystack()
        amount = int(order.total_amount * 100)  # Convert amount to kobo
        try:
            response = paystack.initialize_payment(email=request.user.email, amount=amount)
            logger.info(f"Payment initialization response: {response}")
        except Exception as e:
            logger.error(f"Error initializing payment for user {request.user.username}: {e}")
            return Response({"error": "An error occurred during payment initialization."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response['status']:
            try:
                # Send SMS notification
                twilio.send_sms_notification(to=request.user.phone_no, message=f"Your payment of {order.total_amount} has been initialized. Please click on the link to complete payment request: {response['data']['authorization_url']}")
                logger.info(f"SMS notification sent to {request.user.phone_no}.")
            except Exception as e:
                logger.error(f"Error sending SMS to user {request.user.username}: {e}")
                return Response({"error": "Error sending payment notification."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save payment record
            try:
                payment = Payment.objects.create(
                    user=request.user,
                    order=order,
                    amount=order.total_amount,
                    ref=response['data']['reference']
                )
                logger.info(f"Payment record created for user {request.user.username}.")
            except Exception as e:
                logger.error(f"Error creating payment record for user {request.user.username}: {e}")
                return Response({"error": "Error creating payment record."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = PaymentSerializer(payment)
            return Response({
                "payment": serializer.data,
                "payment_url": response['data']['authorization_url']
            }, status=status.HTTP_200_OK)

        logger.error(f"Payment initialization failed: {response['message']}")
        return Response({"error": response['message']}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(APIView):
    """ 
    Verify payment for an order.

    Endpoint: 
    POST /payments/verify/{payment_ref} -> Verify Payment
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request, reference):
        try:
            payment = Payment.objects.get(ref=reference, user=request.user)
            logger.info(f"Payment record found for reference {reference}.")
        except Payment.DoesNotExist:
            logger.error(f"Payment record not found for reference {reference}.")
            return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

        paystack = Paystack()
        try:
            response = paystack.verify_payment(reference=reference)
            logger.info(f"Payment verification response: {response}")
        except Exception as e:
            logger.error(f"Error verifying payment for reference {reference}: {e}")
            return Response({"error": "Error verifying payment."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response['status']:
            # Update payment and order status
            try:
                payment.status = 'PAID'
                payment.save()
                payment.order.status = 'PAID'
                payment.order.save()
                logger.info(f"Payment status updated for reference {reference}.")
            except Exception as e:
                logger.error(f"Error updating payment/order status for reference {reference}: {e}")
                return Response({"error": "Error updating payment/order status."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Create a notification
            try:
                Notifications.objects.create(
                    title='Payment Successful',
                    message=f'Payment of {payment.amount} for order {payment.order.id} was successful',
                    user=request.user)
                logger.info(f"Payment success notification created for user {request.user.username}.")
            except Exception as e:
                logger.error(f"Error creating notification for payment success: {e}")

            # Send SMS notification
            try:
                twilio.send_sms_notification(to=request.user.phone_no, message=f"Your payment of {payment.amount} has been successful. Thank you for your patronage.")
                logger.info(f"SMS notification sent to {request.user.phone_no}.")
            except Exception as e:
                logger.error(f"Error sending SMS notification for payment success: {e}")

            return Response({"message": "Payment verified successfully!"}, status=status.HTTP_200_OK)

        # Handle payment failure
        payment.status = 'FAILED'
        try:
            Notifications.objects.create(
                title='Payment Failed',
                message=f'Your Payment Failed for order {payment.order.id}',
                user=request.user)
            logger.info(f"Payment failed notification created for user {request.user.username}.")
        except Exception as e:
            logger.error(f"Error creating notification for payment failure: {e}")

        # Send SMS notification
        try:
            twilio.send_sms_notification(to=request.user.phone_no, message=f"Your payment of {payment.amount} has failed. Please click on the link to complete payment request: {response['data']['authorization_url']}")
            logger.info(f"SMS notification sent to {request.user.phone_no}.")
        except Exception as e:
            logger.error(f"Error sending SMS notification for payment failure: {e}")

        payment.save()
        return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)


class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        event = json.loads(request.body)
        logger.info(f"Received webhook event: {event}")

        try:
            if event.get('event') == 'charge.success':
                reference = event['data']['reference']
                try:
                    order = Order.objects.get(payment_reference=reference)
                    order.status = 'PAID'
                    order.save()
                    logger.info(f"Order {order.id} status updated to 'PAID'.")
                except Order.DoesNotExist:
                    logger.warning(f"Order not found for reference {reference}.")
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
        
        return Response({"status": "success"}, status=200)
