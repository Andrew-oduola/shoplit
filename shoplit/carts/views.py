import logging
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException, ValidationError
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartItemSerializer, CartSerializer

logger = logging.getLogger(__name__)

class CartItemViewSet(ModelViewSet):
    """
    Handles operations for CartItem model.

    Endpoints:
        - GET    /cart/items/         -> List all items in the user's cart.
        - POST   /cart/items/         -> Add a new item to the cart.
        - GET    /cart/items/{id}/    -> Retrieve a specific cart item.
        - PUT    /cart/items/{id}/    -> Update a specific cart item.
        - DELETE /cart/items/{id}/    -> Delete a cart item.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)  # Retrieve or create user's cart
        logger.info("Fetched cart for user %s with %d items.", self.request.user, cart.items.count())
        return cart.items.all()

    def create(self, request, *args, **kwargs):
        logger.info("User %s is attempting to add item to cart.", request.user)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.warning("Product with ID %s not found for user %s.", product_id, request.user)
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Add or update item in cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += int(quantity)
                logger.info("Updated quantity of product ID %s in cart for user %s.", product_id, request.user)
            else:
                cart_item.quantity = int(quantity)
                logger.info("Added product ID %s to cart for user %s.", product_id, request.user)
            cart_item.save()

            serializer = self.get_serializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ve:
            logger.error("Validation error while adding product ID %s to cart for user %s: %s", product_id, request.user, ve.detail)
            raise
        except Exception as e:
            logger.error("Unexpected error while adding product ID %s to cart for user %s: %s", product_id, request.user, str(e), exc_info=True)
            raise APIException("An error occurred while adding the product to the cart.")

    def destroy(self, request, *args, **kwargs):
        logger.info("User %s is attempting to remove item from cart.", request.user)
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info("Cart item removed successfully for user %s.", request.user)
            return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            logger.warning("Attempted to delete a non-existent cart item for user %s.", request.user)
            raise APIException("Cart item not found.")
        except Exception as e:
            logger.error("Unexpected error while removing cart item for user %s: %s", request.user, str(e), exc_info=True)
            raise APIException("An error occurred while removing the cart item.")


class CartViewSet(ViewSet):
    """
    Handles operations for Cart model.

    Endpoints:
        - GET    /cart/                  -> Show the user's cart.
        - GET    /cart/total_price/      -> Return the cart's total price.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def list(self, request):
        logger.info("User %s requested cart details.", request.user)
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            logger.info("Cart details retrieved successfully for user %s.", request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error("Unexpected error while fetching cart details for user %s: %s", request.user, str(e), exc_info=True)
            raise APIException("An error occurred while fetching the cart details.")

    @action(detail=False, methods=['get'])
    def total_price(self, request):
        logger.info("User %s requested total price of the cart.", request.user)
        try:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            logger.info("Cart total price calculated successfully for user %s: %s", request.user, cart.total_price)
            return Response({'total_price': cart.total_price})
        except Exception as e:
            logger.error("Unexpected error while calculating total price for user %s: %s", request.user, str(e), exc_info=True)
            raise APIException("An error occurred while calculating the cart's total price.")
