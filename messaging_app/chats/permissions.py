from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions allowed for authenticated users
        if request.method in SAFE_METHODS:
            return request.user in obj.participants.all()

        # Explicitly handle write methods (PUT, PATCH, DELETE)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()

        # For other cases (e.g., creating a message)
        return request.user in obj.participants.all()
