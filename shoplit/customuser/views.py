from rest_framework.viewsets import ModelViewSet

from .models import CustomUser, Vendor

from .serializers import VendorSerializer

# Create your views here.
class VendorViewset(ModelViewSet):
    """
    Handles operations for Vendor model.

    Endpoints:
        - GET    /vendors/        -> List all categories if user is an admin and user vendor if not.
        - POST   /vendors/        -> Create a new vendor.
        - GET    /vendors/{id}/   -> Retrieve a specific vendor.
        - PUT    /vendors/{id}/   -> Update a specific vendor.
        - PATCH  /vendors/{id}/   -> Partially update a vendor.
        - DELETE /vendors/{id}/   -> Delete a vendor.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_queryset(self):
        """
        Customize the queryset based on user type.
        For example, only admins or the vendor themselves can view their details.
        """
        user = self.request.user
        if user.is_superuser:  # Admins can see all vendors
            return Vendor.objects.all()
        if hasattr(user, 'vendor'):  # If the user is a vendor, show their details
            return Vendor.objects.filter(user=user)
        return Vendor.objects.none()  # No access for other users

    def perform_create(self, serializer):
        """
        Customize how vendors are created.
        For example, associate the authenticated user with the vendor.
        """
        serializer.save(user=self.request.user)