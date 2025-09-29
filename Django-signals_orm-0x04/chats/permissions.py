from rest_framework.permissions import BasePermission, SAFE_METHODS


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
