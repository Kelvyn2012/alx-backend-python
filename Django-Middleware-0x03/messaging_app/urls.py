from django.contrib import admin
from django.urls import path, include
from chats import auth

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),
    path("api-auth/", include("rest_framework.urls")),  # ✅ required for browsable API
    # JWT endpoints
    path("api/token/", auth.TokenObtainPair, name="token_obtain_pair"),
    path("api/token/refresh/", auth.TokenRefresh, name="token_refresh"),
]
