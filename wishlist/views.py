import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .serializers import WishListSerializer
from .models import WishList

from drf_spectacular.utils import extend_schema, extend_schema_view

# Initialize logger
logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="List all wishlists or a user's wishlist",
        description="Retrieve a list of all wishlists or filter by user.",
        tags=['Wishlists']
    ),
    create=extend_schema(
        summary="Create a new wishlist",
        description="Submit a new wishlist for a user.",
        request=WishListSerializer,
        responses={status.HTTP_201_CREATED: WishListSerializer},
        tags=['Wishlists']
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific wishlist",
        description="Get details of a specific wishlist by its ID.",
        tags=['Wishlists']
    ),
    update=extend_schema(
        summary="Update a specific wishlist",
        description="Modify an existing wishlist by its ID.",
        request=WishListSerializer,
        responses={status.HTTP_200_OK: WishListSerializer},
        tags=['Wishlists']
    ),
    partial_update=extend_schema(
        summary="Partially update a specific wishlist",
        description="Partially modify an existing wishlist by its ID.",
        request=WishListSerializer,
        responses={status.HTTP_200_OK: WishListSerializer},
        tags=['Wishlists']
    ),
    destroy=extend_schema(
        summary="Delete a specific wishlist",
        description="Remove a wishlist by its ID.",
        responses={status.HTTP_204_NO_CONTENT: None},
        tags=['Wishlists']
    ),
)
class WishListViewSet(viewsets.ModelViewSet):
    """
    Handles the WishList Model

    Endpoints
    GET /wishlists/ -> List all the product in the wishlists of a user and all users if user is superuser
    POST /wishlists/ -> Create a new wishlist for a user
    PUT /wishlists/{id} -> Update a wishlist
    DELETE /wishlists/{id} -> Delete a wishlist
    """
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        try:
            # If the user is a superuser, return all wishlists
            if self.request.user.is_superuser:
                return self.queryset.all()
            else:
                return self.queryset.filter(user=self.request.user)
        except Exception as e:
            logger.error(f"Error fetching wishlist for user {self.request.user.id}: {e}")
            raise NotFound(detail="Error retrieving the wishlist.")

    def perform_create(self, serializer):
        try:
            # Automatically associate the logged-in user with the wishlist
            serializer.save(user=self.request.user)
            logger.info(f"Wishlist created by user {self.request.user.id} for product {serializer.validated_data['product']}")
        except Exception as e:
            logger.error(f"Error creating wishlist for user {self.request.user.id}: {e}")
            raise ValidationError("Error saving the wishlist.")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error during wishlist creation: {e}")
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during wishlist creation: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except NotFound:
            logger.error(f"Wishlist not found for update with ID {kwargs.get('pk')}")
            return Response({"error": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error during wishlist update: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except NotFound:
            logger.error(f"Wishlist not found for deletion with ID {kwargs.get('pk')}")
            return Response({"error": "Wishlist not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error during wishlist deletion: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
