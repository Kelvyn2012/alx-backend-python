from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet
from chats import auth

# main router
router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")

# nested router: messages belong to conversations
conversations_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
conversations_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
    path("api/token/", auth.TokenObtainPair, name="token_obtain_pair"),
    path("api/token/refresh/", auth.TokenRefresh, name="token_refresh"),
]
