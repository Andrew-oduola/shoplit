from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


from .models import Order
from .serializers import OrderSerializers

# Create your views here.
class OrderViewSet(ModelViewSet):
    """
    Handles operations for Order model.

    Endpoints:
        - GET    /orders        -> List all orders by the user.
        - POST   /orders/        -> Create a new order for the user.
        - GET    /orders/{id}/   -> Retrieve a specific order.
        - PUT    /orders/{id}/   -> Update a specific order.
        - PATCH  /orders/{id}/   -> Patch update on a specific order.
        - DELETE /orders/{id}/   -> Delete a order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        #Ensure you are only returning the user's order
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign the login user to the order
        print('Calling serializer from viewset')
        serializer.save(user=self.request.user)
