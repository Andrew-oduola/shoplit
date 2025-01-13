import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import VendorSerializer

# Configure logger
logger = logging.getLogger(__name__)

class VendorViewset(ModelViewSet):
    """
    Handles operations for Vendor model.

    Endpoints:
        - GET    /vendors/        -> List all vendors if user is an admin, or the vendor's details if not.
        - POST   /vendors/        -> Create a new vendor (linked to the authenticated user).
        - GET    /vendors/{id}/   -> Retrieve a specific vendor.
        - PUT    /vendors/{id}/   -> Update a specific vendor.
        - PATCH  /vendors/{id}/   -> Partially update a vendor.
        - DELETE /vendors/{id}/   -> Delete a vendor.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Customize the queryset based on the user type.
        - Admins can view all vendors.
        - Vendors can view only their details.
        - Other users do not have access to this resource.
        """
        user = self.request.user

        try:
            if user.is_superuser:  # Admin users
                logger.info(f"Admin user {user.username} accessed all vendor details.")
                return Vendor.objects.all()

            if hasattr(user, 'vendor'):  # Vendor users
                logger.info(f"Vendor user {user.username} accessed their vendor details.")
                return Vendor.objects.filter(user=user)

            logger.warning(f"Unauthorized access attempt by user {user.username}.")
            return Vendor.objects.none()

        except Exception as e:
            logger.error(f"Error retrieving queryset for user {user.username}: {e}")
            return Vendor.objects.none()

    def perform_create(self, serializer):
        """
        Customize vendor creation by associating the vendor with the authenticated user.
        Ensures that each user can create only one vendor profile.
        """
        user = self.request.user

        try:
            # Check if the user already has a vendor profile.
            if hasattr(user, 'vendor'):
                logger.error(f"User {user.username} attempted to create a duplicate vendor profile.")
                return Response(
                    {"error": "A vendor profile already exists for this user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(user=user)
            logger.info(f"Vendor profile created for user {user.username}.")
        
        except Exception as e:
            logger.error(f"Error creating vendor profile for user {user.username}: {e}")
            return Response(
                {"error": "An error occurred while creating the vendor profile."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Customize vendor deletion to ensure:
        - Admins can delete any vendor.
        - Vendors can delete only their profile.
        """
        try:
            instance = self.get_object()
            user = self.request.user

            # Check permissions for deletion.
            if not user.is_superuser and instance.user != user:
                logger.error(
                    f"Unauthorized delete attempt by user {user.username} "
                    f"for vendor {instance.id}."
                )
                return Response(
                    {"error": "You do not have permission to delete this vendor."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Proceed with deletion.
            self.perform_destroy(instance)
            logger.info(f"Vendor {instance.id} deleted by user {user.username}.")
            return Response(
                {"message": "Vendor deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        except Vendor.DoesNotExist:
            logger.error(f"Vendor not found for deletion. ID: {kwargs.get('pk')}")
            return Response(
                {"error": "Vendor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            logger.error(f"Error deleting vendor {kwargs.get('pk')} by user {user.username}: {e}")
            return Response(
                {"error": "An error occurred while deleting the vendor."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
