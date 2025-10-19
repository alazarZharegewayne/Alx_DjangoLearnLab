from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    """
    Model for user notifications
    """
    # Notification types
    FOLLOW = 'follow'
    LIKE = 'like'
    COMMENT = 'comment'
    
    NOTIFICATION_TYPES = [
        (FOLLOW, 'Follow'),
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    verb = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    # Generic foreign key for the target object (post, comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"

    @property
    def message(self):
        """Generate a human-readable notification message"""
        if self.verb == self.FOLLOW:
            return f"{self.actor.username} started following you"
        elif self.verb == self.LIKE:
            return f"{self.actor.username} liked your post"
        elif self.verb == self.COMMENT:
            return f"{self.actor.username} commented on your post"
        return f"{self.actor.username} {self.verb}"