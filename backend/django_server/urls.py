from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('django.contrib.auth.urls')),

    # USER RELATED PATH #
    path('api/', include('src.urls.UserUrl')),

    # AUTH RELATED PATH
    path('api/auth/', include('src.urls.AuthUrl')),

    # SPOTIFY RELATED PATH #
    path('api/spotify/auth/', include('src.urls.SpotifyAuthUrl')),

    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Interface Swagger UI (celle que vous voulez)
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # Interface ReDoc (alternative)
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]