from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.
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

    def get_queryset(self):
        # Optionally 
        product_id = self.request.query_params.get('product')
        if product_id:
            return self.queryset.filter(product_id=product_id)
        return self.queryset
    
    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the review
        serializer.save(user=self.request.user)

    
    
