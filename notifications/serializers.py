from rest_framework.serializers import ModelSerializer
from .models import Notifications


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'user', 'title', 'message', 'created_at', 'updated_at', 'is_read']


class NoticationMiniSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'user', 'title', 'message']


class NotificationCreateSerializer(ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['user', 'title', 'message']