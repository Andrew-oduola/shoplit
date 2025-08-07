import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializers

from drf_spectacular.utils import extend_schema, extend_schema_view

# Configure logger
logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        summary="List all orders",
        description="Retrieve a list of all orders made by the user.",
        tags=["Orders"]
    ),
    create=extend_schema(
        summary="Create a new order",
        description="Create a new order for the user.",
        tags=["Orders"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific order",
        description="Get details of a specific order by its ID.",
        tags=["Orders"]
    ),
    update=extend_schema(
        summary="Update a specific order",
        description="Update the details of a specific order.",
        tags=["Orders"]
    ),
    partial_update=extend_schema(
        summary="Partially update an order",
        description="Partially update the details of a specific order.",
        tags=["Orders"]
    ),
    destroy=extend_schema(
        summary="Delete an order",
        description="Delete a specific order by its ID.",
        tags=["Orders"]
    )
)
class OrderViewSet(ModelViewSet):
    """
    Handles operations for the Order model.

    Endpoints:
        - GET    /orders        -> List all orders by the user.
        - POST   /orders/       -> Create a new order for the user.
        - GET    /orders/{id}/  -> Retrieve a specific order.
        - PUT    /orders/{id}/  -> Update a specific order.
        - PATCH  /orders/{id}/  -> Patch update on a specific order.
        - DELETE /orders/{id}/  -> Delete an order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        """
        Ensure only the user's orders are returned.
        """
        try:
            queryset = self.queryset.filter(user=self.request.user)
            logger.info(f"Orders retrieved for user {self.request.user.username}.")
            return queryset
        except Exception as e:
            logger.error(f"Error retrieving orders for user {self.request.user.username}: {e}")
            return Order.objects.none()

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the order when creating.
        """
        try:
            logger.info(f"Creating order for user {self.request.user.username}.")
            serializer.save(user=self.request.user)
            logger.info(f"Order created successfully for user {self.request.user.username}.")
        except Exception as e:
            logger.error(f"Error creating order for user {self.request.user.username}: {e}")
            raise Exception(f"An error occurred while creating the order: {e}")

    def update(self, request, *args, **kwargs):
        """
        Custom update method with additional error handling.
        """
        try:
            order = self.get_object()
            if order.user != request.user:
                logger.warning(f"Unauthorized update attempt by user {request.user.username} on order {order.id}.")
                return Response({"error": "You cannot update this order."}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f"Order {order.id} updated successfully by user {request.user.username}.")
            return Response(serializer.data)
        
        except Exception as e:
            logger.error(f"Error updating order {kwargs.get('pk')} for user {request.user.username}: {e}")
            return Response(
                {"error": f"An error occurred while updating the order: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Custom delete method with additional error handling.
        """
        try:
            order = self.get_object()
            if order.user != request.user:
                logger.warning(f"Unauthorized delete attempt by user {request.user.username} on order {order.id}.")
                return Response({"error": "You cannot delete this order."}, status=status.HTTP_403_FORBIDDEN)

            order.delete()
            logger.info(f"Order {order.id} deleted successfully by user {request.user.username}.")
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            logger.error(f"Error deleting order {kwargs.get('pk')} for user {request.user.username}: {e}")
            return Response(
                {"error": f"An error occurred while deleting the order: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
