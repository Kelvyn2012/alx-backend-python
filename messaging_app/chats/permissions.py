from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Conversation object
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Message object
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()
        return False
