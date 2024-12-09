from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializers

# Create your views here.
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #Ensure you are only returning the user's order
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign the login user to the order
        print('Calling serializer from viewset')
        serializer.save(user=self.request.user)

    # @action(detail=True, methods=['post'])
    # def initialize_payment(self, request, pk=None):
    #     """
    #     Initialize a payment for the order
    #     """
    #     order = self.get_object()
    #     paystack = Paystack()

    #     # Calculate total amount (in kobo)
    #     amount = int(order.total_amount * 100)  # Convert to kobo

    #     # Initialize payment
    #     response = paystack.initialize_payment(email=request.user.email, amount=amount)
    #     if response['status']:
    #         # Save the payment reference to the order
    #         order.payment_reference = response['data']['reference']
    #         order.save()

    #         return Response({
    #             "payment_url": response['data']['authorization_url'],
    #             "reference": response['data']['reference']
    #         }, status=status.HTTP_200_OK)

    #     return Response({"error": response['message']}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['post'])
    # def verify_payment(self, request, pk=None):
    #     """
    #     Verify payment for the order
    #     """
    #     order = self.get_object()
    #     paystack = Paystack()

    #     # Verify payment
    #     response = paystack.verify_payment(reference=order.payment_reference)
    #     if response['status']:
    #         # Update order status if payment was successful
    #         order.status = 'PAID'
    #         order.save()
    #         return Response({"message": "Payment verified successfully!"}, status=status.HTTP_200_OK)

    #     # Mark order as failed if payment verification fails
    #     order.status = 'FAILED'
    #     order.save()
    #     return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)