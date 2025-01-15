import logging
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Notifications
from .serializers import (
    NotificationSerializer,
    NoticationMiniSerializer,
    NotificationCreateSerializer,
)

# Configure logger
logger = logging.getLogger(__name__)

class NotificationsViewSet(ModelViewSet):
    """
    Handles operations for Notifications model.
    """
    queryset = Notifications.objects.all()
    serializer_class = NoticationMiniSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'is_read']

    def create(self, request, *args, **kwargs):
        """
        Handle notification creation.
        """
        try:
            serializer = NotificationCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f"Notification created successfully by user {request.user}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return Response(
                {"error": "An error occurred while creating the notification."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieving a single notification.
        """
        try:
            instance = self.get_object()
            serializer = NotificationSerializer(instance)
            logger.info(f"Notification {instance.id} retrieved by user {request.user}.")
            return Response(serializer.data)

        except Notifications.DoesNotExist:
            logger.error(f"Notification not found for ID {kwargs.get('pk')}.")
            return Response(
                {"error": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        except Exception as e:
            logger.error(f"Error retrieving notification {kwargs.get('pk')}: {e}")
            return Response(
                {"error": "An error occurred while retrieving the notification."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    def list(self, request, *args, **kwargs):
        """
        Handle listing notifications.
        """
        try:
            queryset = Notifications.objects.all()
            if not request.user.is_staff:
                queryset = queryset.filter(user=request.user)
                logger.info(f"User {request.user} listed their notifications.")
            else:
                logger.info("Admin user listed all notifications.")

            serializer = NoticationMiniSerializer(queryset, many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error listing notifications for user {request.user}: {e}")
            return Response(
                {"error": "An error occurred while listing notifications."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
