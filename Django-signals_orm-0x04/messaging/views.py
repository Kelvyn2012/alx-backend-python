from django.contrib.auth import get_user_model, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

User = get_user_model()


@login_required
def delete_user(request):
    """Allow a logged-in user to delete their account"""
    if request.method == "POST":
        user = request.user
        username = user.username
        logout(request)  # log them out before deleting
        user.delete()  # this triggers post_delete signal
        return HttpResponse(f"User {username} and related data deleted successfully.")
    return HttpResponse(
        "Invalid request. Please submit a POST request to delete your account."
    )
