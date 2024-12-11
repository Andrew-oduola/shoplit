# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from .models import Payment
# from orders.models import Order

# from django.http import JsonResponse
# from carts.models import Cart

# # Create your views here.
# def verify_payment(request, ref):
#     try:
#         cart = Cart(request)
#         payment = Payment.objects.get(ref=ref)
#         verified = payment.verify_payment()

#         if verified:
#             last_order = Order.objects.latest('created_at')

#             if last_order:
#                 order = get_object_or_404(Order, pk=last_order.id)
#                 order.paid = True
#                 order.save()

#                 order_info = {
#                     'id': order.id,
#                     'total_cost': order.total_cost
#                 }

#                 context = {
#                     'placed_order': order_info,
#                     'payment': payment
#                 }
#                 cart.clear()
#                 return render()
#             else:
#                 return JsonResponse({"error message": "Order ID not found"})
#         else:
#             return redirect('/')
#     except Payment.DoesNotExist:
#         return JsonResponse({"error message": "Payment not found"})



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json

from .models import Payment
from .serializers import PaymentSerializer
from .paystack import Paystack
from orders.models import Order  # Import your Order model

class InitializePaymentView(APIView):
    """ 
    Initialize payment for an order.

    Endpoint: 
    POST /payments/initialize/{order_id}// -> Initialize Payment
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        paystack = Paystack()
        amount = int(order.total_amount * 100)  # Convert amount to kobo
        response = paystack.initialize_payment(email=request.user.email, amount=amount)

        if response['status']:
            # Save payment record
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_amount,
                ref=response['data']['reference']
            )
            serializer = PaymentSerializer(payment)
            return Response({
                "payment": serializer.data,
                "payment_url": response['data']['authorization_url']
            }, status=status.HTTP_200_OK)

        return Response({"error": response['message']}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPaymentView(APIView):
    """ 
    Initialize payment for an order.

    Endpoint: 
    POST /payments/verify/{payment ref}// -> Verify Payment
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, reference):
        try:
            payment = Payment.objects.get(ref=reference, user=request.user)
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found."}, status=status.HTTP_404_NOT_FOUND)

        paystack = Paystack()
        response = paystack.verify_payment(reference=reference)

        if response['status']:
            # Update payment and order status
            payment.status = 'PAID'
            payment.save()
            payment.order.status = 'PAID'
            payment.order.save()

            return Response({"message": "Payment verified successfully!"}, status=status.HTTP_200_OK)

        payment.status = 'FAILED'
        payment.save()
        return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)



class PaystackWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        event = json.loads(request.body)
        if event.get('event') == 'charge.success':
            reference = event['data']['reference']
            # Update the corresponding order status
            try:
                order = Order.objects.get(payment_reference=reference)
                order.status = 'PAID'
                order.save()
            except Order.DoesNotExist:
                pass
        return Response({"status": "success"}, status=200)
