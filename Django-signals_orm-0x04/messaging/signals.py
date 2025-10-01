from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification for the receiver when a new message is sent."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log old content before a message is updated"""
    if not instance.pk:  # new message, skip
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content is being changed
    if old_message.content != instance.content:
        # Save old content into history
        MessageHistory.objects.create(message=instance, old_content=old_message.content)
        # Mark the message as edited
        instance.edited = True
