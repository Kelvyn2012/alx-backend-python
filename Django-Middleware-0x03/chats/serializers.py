from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "created_at",
            "email",
            "phone_number",
            "role",
            "full_name",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)  # or customize
    conversation_id = serializers.UUIDField(
        source="conversation.conversation_id", read_only=True
    )

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "conversation_id",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["sender", "conversation_id", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="message_set")

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "created_at",
            "messages",
            "participants",
        ]

    def validate(self, data):
        participants = self.initial_data.get("participants", [])
        if len(participants) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants."
            )
        return data
