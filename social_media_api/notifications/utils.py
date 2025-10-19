from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(recipient, actor, verb, target=None):
    """
    Utility function to create notifications
    """
    notification = Notification(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target=target
    )
    notification.save()
    return notification

def create_follow_notification(followed_user, follower):
    """Create notification for follow action"""
    return create_notification(
        recipient=followed_user,
        actor=follower,
        verb=Notification.FOLLOW
    )

def create_like_notification(post_author, liker, post):
    """Create notification for like action"""
    return create_notification(
        recipient=post_author,
        actor=liker,
        verb=Notification.LIKE,
        target=post
    )

def create_comment_notification(post_author, commenter, post):
    """Create notification for comment action"""
    return create_notification(
        recipient=post_author,
        actor=commenter,
        verb=Notification.COMMENT,
        target=post
    )