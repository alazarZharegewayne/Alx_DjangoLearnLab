from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer

class NotificationListView(generics.ListAPIView):
    """
    View for listing user notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class UnreadNotificationListView(generics.ListAPIView):
    """
    View for listing unread user notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user, read=False)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """
    Mark a notification as read
    """
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    
    if notification.read:
        return Response(
            {'error': 'Notification is already read'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    notification.read = True
    notification.save()
    
    serializer = NotificationSerializer(notification)
    return Response({
        'message': 'Notification marked as read',
        'notification': serializer.data
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all user notifications as read
    """
    unread_notifications = Notification.objects.filter(recipient=request.user, read=False)
    count = unread_notifications.count()
    
    unread_notifications.update(read=True)
    
    return Response({
        'message': f'Marked {count} notifications as read'
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """
    Get notification statistics for the current user
    """
    total_notifications = Notification.objects.filter(recipient=request.user).count()
    unread_count = Notification.objects.filter(recipient=request.user, read=False).count()
    
    return Response({
        'total_notifications': total_notifications,
        'unread_count': unread_count
    })