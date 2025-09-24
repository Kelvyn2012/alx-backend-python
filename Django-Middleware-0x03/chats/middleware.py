# chats/middleware.py
import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")

        # Prevent adding multiple handlers on autoreload
        if not self.logger.handlers:
            handler = logging.FileHandler("requests.log")
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user.username
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = "Guest"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        # Always call the next middleware / view
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour
        # Restrict access outside 6PM–9PM (18:00–21:00)
        if current_hour < 18 or current_hour >= 23:
            return HttpResponseForbidden("Chat access is restricted during this time")
        # Continue normally if within allowed hours
        response = self.get_response(request)
        return response


# chats/middleware.py
import time
from collections import defaultdict
from django.http import HttpResponseForbidden


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_history = defaultdict(list)

        # Rate limit config
        self.limit = 5  # max messages
        self.time_window = 60  # seconds (1 minute)

        # Offensive words list
        self.banned_words = {"badword", "offensive", "curse", "hate", "kill", "fuckyou"}

        # Logger setup
        self.logger = logging.getLogger("offensive_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        # Apply only to chat POST requests
        if request.method == "POST" and "/conversations/" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # --- 1. Rate limiting check ---
            self.message_history[ip] = [
                ts for ts in self.message_history[ip] if now - ts < self.time_window
            ]
            # --- log the incoming request ---
            self.logger.info(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - IP: {ip} - Path: {request.path}"
            )

            if len(self.message_history[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Message limit exceeded. Please wait before sending more."
                )

            # Record message timestamp
            self.message_history[ip].append(now)

            # --- 2. Offensive language check ---
            body = request.POST.get("message_body", "")  # message field
            if any(bad_word in body.lower() for bad_word in self.banned_words):
                return HttpResponseForbidden(
                    "Your message contains offensive language and was blocked."
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extract client IP address (handles proxies if needed)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths with allowed roles
        self.role_permissions = {
            "/admin/": {"admin"},
            "/conversations/delete/": {"admin"},
            "/conversations/create/": {"admin", "host"},
            "/conversations/moderate/": {"admin"},
        }

    def __call__(self, request):
        for path, allowed_roles in self.role_permissions.items():
            if request.path.startswith(path):
                user = request.user

                if not user.is_authenticated:
                    return HttpResponseForbidden("Authentication required.")

                if getattr(user, "role", None) in allowed_roles:
                    return self.get_response(request)

                return HttpResponseForbidden(
                    "You do not have permission to access this resource."
                )

        # If path not protected → allow
        return self.get_response(request)
