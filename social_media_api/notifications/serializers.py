from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    message = serializers.CharField(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'actor_username', 'verb',
            'target', 'read', 'created_at', 'message'
        ]
        read_only_fields = ['id', 'created_at']

class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['read']