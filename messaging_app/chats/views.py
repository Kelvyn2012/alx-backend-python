from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer, ConversationSerializer
from .models import Conversation, Message

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    """
        Create a new conversation with given participants.
        Example payload:
        {
            "participants": [1, 2]   # user IDs
        }
        """

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        if len(participants) < 2:
            return Response(
                {"error": "A conversation must have at least two participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(pk__in=participants))
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        sender_id = request.data.get("sender_id")
        message_body = request.data.get("message_body")
        if not conversation_id or not message_body or not sender_id:
            return Response(
                {"error": "conversation_id, sender_id and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            sender = User.objects.get(pk=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Sender not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        message = Message.objects.create(
            conversation=conversation, sender=sender, message_body=message_body
        )
        serializer = self.get_serializer(message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
