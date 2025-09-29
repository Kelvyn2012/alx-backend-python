from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessagingSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="test123")
        self.receiver = User.objects.create_user(username="bob", password="test123")

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Hello Bob!"
        )
        notification = Notification.objects.get(user=self.receiver, message=message)

        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
