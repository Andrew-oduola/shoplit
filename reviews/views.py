import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import Review
from .serializers import ReviewSerializer

# Initialize logger
logger = logging.getLogger(__name__)

class ReviewViewSet(ModelViewSet):
    """
    Handles the review Model

    Endpoints: 
    GET   /reviews/ -> List all reviews
    GET   /reviews/?product={product_id} -> List all reviews for a specific product
    POST  /reviews/ -> Create a new review for a specific product
    GET   /reviews/{id}/ -> Retrieve a specific review
    PUT   /reviews/{id}/ -> Update a specific review
    DELETE /reviews/{id}/ -> Delete a specific review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        # Optionally filter by product_id if passed in query parameters
        product_id = self.request.query_params.get('product')
        if product_id:
            try:
                # Check if the product exists
                return self.queryset.filter(product_id=product_id)
            except Exception as e:
                logger.error(f"Error fetching reviews for product {product_id}: {e}")
                raise NotFound(detail="Product not found.")
        return self.queryset

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the review
        try:
            serializer.save(user=self.request.user)
            logger.info(f"Review created by user {self.request.user.id} for product {serializer.validated_data['product']}")
        except Exception as e:
            logger.error(f"Error creating review for user {self.request.user.id}: {e}")
            raise ValidationError("Error saving the review.")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error during review creation: {e}")
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during review creation: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except NotFound:
            logger.error(f"Review not found for update with ID {kwargs.get('pk')}")
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error during review update: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except NotFound:
            logger.error(f"Review not found for deletion with ID {kwargs.get('pk')}")
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Unexpected error during review deletion: {e}")
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
