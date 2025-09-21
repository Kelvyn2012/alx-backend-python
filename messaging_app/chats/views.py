from rest_framework import viewsets, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["participants__username"]  # search by participant username
    ordering_fields = ["created_at"]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__username"]  # search by content or sender
    ordering_fields = ["sent_at"]
