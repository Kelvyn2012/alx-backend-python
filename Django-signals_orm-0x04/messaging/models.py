from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # ✅ flag for edited messages
    edited_by = models.ForeignKey(  # ✅ who last edited
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
    )
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"from {self.sender} to {self.receiver}: {self.content[:20]}"

    """ Recursive function to fetch replies """

    def get_thread(self):
        """Fetch this message and all its replies recursively"""
        thread = [self]
        for reply in self.replies.all().select_related("sender", "receiver"):
            thread.extend(reply.get_thread())
        return thread


class MessageHistory(models.Model):
    """Stores previous versions of a message before edits"""

    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.TimeField(auto_now_add=True)
    edited_by = models.ForeignKey(  # ✅ who made the edit
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="message_edits",
    )

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message, related_name="notifacation", on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"
