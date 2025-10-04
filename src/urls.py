from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for my project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="youremail@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(('user_account.urls', 'user_account'), namespace='user_account')),
    path('profile/', include(('profile_users.urls', 'profile_users'), namespace='profile')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('ai/', include(('ai_assistant.urls', 'ai_assistant'), namespace='ai_assistant')),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),

    # Swagger / ReDoc
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
