from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


def create_notification(sender, instance, created, **kwargs):
    """Create a notification for the receiver when a new message is sent."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
