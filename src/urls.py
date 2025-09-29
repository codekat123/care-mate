from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('user_account.urls',namespace='user_account')),
    path('profile/',include('profile_users.urls',namespace='profile')),
    path('dashboard/',include('dashboard.urls',namespace='dashboard')),
    path('ai/', include('ai_assistant.urls', namespace='ai_assistant')),
    path('',include('home.urls',namespace='home')),
    path('chat/',include('chat.urls',namespace='chat')),


        # JWT endpoints
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
