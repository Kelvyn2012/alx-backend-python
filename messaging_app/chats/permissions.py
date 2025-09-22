from rest_framework import permissions


class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Allow access only to participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "participants"):  # Conversation
            return request.user in obj.participants.all()
        if hasattr(obj, "conversation"):  # message
            return request.user in obj.conversation.participants.all()
        return False
