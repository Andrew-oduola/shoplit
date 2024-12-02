from rest_framework.viewsets import ModelViewSet
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