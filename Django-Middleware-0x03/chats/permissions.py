from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrParticipant(BasePermission):
    """
    - Admin users can access everything.
    - Non-admins must be participants of the conversation/message.
    """

    def has_object_permission(self, request, view, obj):
        # Allow admin full access
        if (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        ):
            return True

        # For Conversations
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # For Messages (check conversation participants)
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False


class IsParticipantOfConversation(BasePermission):
    """
    Only authenticated participants of a conversation
    can view or modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Must be logged in
        if not request.user or not request.user.is_authenticated:
            return False

        # Read-only access
        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()

        # Write access (PUT, PATCH, DELETE)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()

        # Default: user must still be a participant
        return request.user in obj.participants.all()
