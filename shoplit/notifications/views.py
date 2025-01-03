from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import Notifications
from .serializers import NotificationSerializer, NoticationMiniSerializer, NotificationCreateSerializer

# Create your views here.
class NotificationsViewSet(ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NoticationMiniSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = NotificationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = NotificationSerializer(instance)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = NoticationMiniSerializer(queryset, many=True)
        return Response(serializer.data)


