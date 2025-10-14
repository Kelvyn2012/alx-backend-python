from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated, AllowAny
from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import permission_classes


User = get_user_model()


@permission_classes([AllowAny])
def api_home(request):
    return Response({"status": "success", "message": "Messaging API is running 🚀"})


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    search_fields = ["title", "participants__username"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        conversation.participants.add(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    search_fields = ["content", "sender__username"]
    ordering_fields = ["timestamp"]

    def get_queryset(self):
        """Only return messages in conversations the user participates in."""
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new message in the given conversation (from URL)."""
        conversation_id = kwargs.get("conversation_pk")

        if not conversation_id:
            return Response(
                {"detail": "conversation_id is missing from the URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
