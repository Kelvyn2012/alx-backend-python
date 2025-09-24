# chats/middleware.py
import logging
from datetime import datetime


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
