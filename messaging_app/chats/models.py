from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_ROLES = [
        ("guest", "Guest"),
        ("host", "Host"),
        ("admin", "Admin"),
    ]

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="guest")
    created_at = models.DateTimeField(auto_now_add=True)

    # email should be unique, AbstractUser already has email but we enforce uniqueness
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} and ({self.email})"


class Conversation(models.Model):
    """
    Represents a conversation between multiple participants (Users).
    """

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(User, related_name="conversation")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"conversation: {self.conversation_id}"


class Message(models.Model):
    """
    Represents a message sent by a user within a conversation.
    """

    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.TextField()
    sent_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.username}"
