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


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message


@login_required
def send_message(request, receiver_id):
    """Send a new message"""
    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_message")  # optional reply

        parent_message = None
        if parent_id:
            parent_message = get_object_or_404(Message, pk=parent_id)

        Message.objects.create(
            sender=request.user,  # ✅ required for checks
            receiver_id=receiver_id,
            content=content,
            parent_message=parent_message,
        )
        return HttpResponse("Message sent successfully.")
    return HttpResponse("Invalid request. Use POST to send a message.")


@login_required
def conversation_view(request, user_id):
    """View threaded conversation between current user and another user"""
    # ✅ Using select_related & prefetch_related
    messages = (
        (
            Message.objects.filter(sender=request.user, receiver_id=user_id)
            | Message.objects.filter(sender_id=user_id, receiver=request.user)
        )
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
        .filter(parent_message__isnull=True)
    )

    context = {"messages": messages}
    return render(request, "messaging/conversation.html", context)


def get_thread(message):
    """Recursive helper to fetch a message and all replies"""
    thread = [message]
    for reply in message.replies.all().select_related("sender", "receiver"):
        thread.extend(get_thread(reply))
    return thread


@login_required
def message_thread_view(request, message_id):
    """Display a threaded conversation for a single message"""
    message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"), pk=message_id
    )
    thread = get_thread(message)
    context = {"thread": thread}
    return render(request, "messaging/thread.html", context)
