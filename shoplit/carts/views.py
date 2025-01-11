from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartSerializer

# Create your views here.


class CartItemViewSet(ModelViewSet):
    """
    Handles operations for CartItem model.

    Endpoints:
        - GET    /cart/items        -> List all items in the users cart.
        - POST   /cart/items/        -> Add a new item to the cart.
        - GET    /cart/items/{id}/   -> Retrieve a specific cart item.
        - PUT    /cart/items/{id}/   -> Update a specific cart item.
        - DELETE /cart/items/{id}/   -> Delete a cart item.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user) # get the current cart or create a new one if it doesn't exist
        return cart.items.all()
    
    def create(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Add or update item in cart 
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
    
class CartViewSet(ViewSet):
    """
    Handles operations for Cart model.

    Endpoints:
        - GET    /cart/        -> Shows the users cart.
        - GET   /cart/total_price/        -> Returns the cart total price.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def total_price(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response({'total_price': cart.total_price})
